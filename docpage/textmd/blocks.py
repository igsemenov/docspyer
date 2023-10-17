# -*- coding: utf-8 -*-
"""Blocks of Markdown (MD) text.
"""

import re
import html
import textwrap
from docspyer.utils import texttrees
from docspyer.utils import treeashtml
from docspyer.utils import tableashtml
from . import emphase


class MDBlock:
    """Base class for MD blocks.

    Attributes
    ----------
    text : str
        Block text.

    Features
    --------

    (a) Can be converted to HTML: 

        Block().make_html() → str

    (b) Support type checkers:

        is_heading()
        is_list()

    """

    NAME = ''
    VIEW = ''
    SPEC = ''

    def __init__(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def is_heading(self):
        return isinstance(self, MDHeading)

    def is_list(self):
        return isinstance(self, MDList)

    def emphasize(self, text):
        return emphase.edit_inline_md(text)

    def escape_html(self, text):
        return html.escape(text)


class MDHeading(MDBlock):
    """MD heading.

    Attributes
    ----------
    text : str
        Line with a heading.

    """

    NAME = 'Heading'

    RE_PREF = '#{1,}\s'

    VIEW = '# Heading'

    SPEC = f"""
    - Occupies a single line.
    - Must start with `{RE_PREF}`.
    """

    def make_html(self) -> str:
        heading = self.make_html_heading()
        return self.add_toc_anchor_prolog(heading)

    def make_html_heading(self):
        level = self.get_level()
        content = self.get_content()
        return f'<h{level}>{content}</h{level}>'

    def add_toc_anchor_prolog(self, heading):
        return '<div class="toc-anchor"></div>' + heading

    def get_level(self) -> int:
        return str.count(self.text, '#')

    def get_content(self) -> str:
        return str.lstrip(self.text, '# ')


class MDHrule(MDBlock):
    """Horizontal rule.
    """

    NAME = 'Rule'

    RE_HRULE = '[-=\*]{3,}'

    VIEW = ''

    SPEC = f"""
    - Represents a horizontal line.
    - Matches the regexp `{RE_HRULE}`.
    """

    def make_html(self) -> str:
        return self.render_hrule()

    def render_hrule(self):
        return '<hr>'


class MDPar(MDBlock):
    """Ordinary paragraph.

    Parameters
    ----------
    text : str
        Content of the paragraph.

    """

    NAME = 'Par'

    VIEW = """
    Some ordinary paragraph that is 
    not a heading, list, table, ...
    """

    RE_HTML_BLOCK = '<(p|dl|div|svg)'

    COMMENT_START = "<!--"
    COMMENT_END = "-->"

    SPEC = f"""
    - Represents an ordinary piece of text.
    - Dumped to HTML as it is, when is an <i>HTML block</i>.
    
    <i>HTML blocks</i>

    Paragraphs starting with `{RE_HTML_BLOCK}` or HTML comments.

    """

    def make_html(self) -> str:

        res = self.dump_asis_if_to_ignore()

        if res is not None:
            return res

        return self.dump_to_ptag_otherwise()

    def dump_asis_if_to_ignore(self):
        if self.is_to_ignore():
            return self.text
        return None

    def dump_to_ptag_otherwise(self):
        text = self.text
        text = self.emphasize(text)
        return '<p>' + text + '</p>'

    def is_to_ignore(self):
        if self.is_comment(self.text):
            return True
        if self.is_html_block(self.text):
            return True
        return False

    def is_html_block(self, text) -> bool:
        if re.match(self.RE_HTML_BLOCK, text):
            return True
        return False

    def is_comment(self, text):
        if not text.startswith(self.COMMENT_START):
            return False
        if not text.endswith(self.COMMENT_END):
            return False
        return True


class MDList(MDBlock):
    """MD list.

    Attributes
    ----------
    text : str
        Paragraph with a list.

    """

    NAME = 'List'

    ITER = '-\s'

    VIEW = """
    - Alfa
    - Bravo
      - Charlie
        Delta
        - Echo
    """

    SPEC = f"""
    - Must start with the iterator `{ITER}`.
    - Multiline items are allowed, see `Charlie...` item.
    """

    def make_html(self) -> str:

        text = self.text

        text = self.emphasize(text)
        root = self.list_to_tree(text)
        ashtml = self.tree_to_html(root)

        return self.add_css_class(ashtml)

    def list_to_tree(self, text_with_list):
        return texttrees.maketree(text_with_list)

    def tree_to_html(self, root) -> str:
        return treeashtml.dumptree_html(root)

    def add_css_class(self, ashtml):
        return ashtml.replace(
            '<p>\n<ul>', '<p>\n<ul class="md-list">'
        )


class MDTable(MDBlock):
    """MD table.

    Attributes
    ----------
    text : str
        Paragraph with a table.

    """

    NAME = 'Table'

    VIEW = """
    Name  | Info
    ------|--------
    Alfa  | Bravo
    Delta | Charlie
    """

    SPEC = """
    - Follows the <i>one-line-is-one-row</i> structure.
    - Columns are separated by `|`.
    - The first row is a table head.
    """

    def make_html(self) -> str:

        text = self.text
        text = self.emphasize(text)

        columns = self.fetch_columns(text)
        return self.run_maketable_html(columns)

    def fetch_columns(self, text) -> list[list[str]]:
        rows = self.fetch_rows(text)
        return self.rows_to_columns(rows)

    def fetch_rows(self, text) -> list[list[str]]:

        def get_allrows(text):
            return [
                line.strip('|').split('|') for line in text.splitlines()
            ]

        def del_underline(rows):
            return [
                rows[0], *rows[2::]
            ]

        rows = get_allrows(text)
        rows = del_underline(rows)

        return rows

    def rows_to_columns(self, rows) -> list[list[str]]:

        def getcolumn(rows):
            return list(
                map(list.pop, rows)
            )

        rows = [
            list(reversed(row)) for row in rows
        ]

        minlen = min(map(len, rows))

        return [
            getcolumn(rows) for i in range(minlen)
        ]

    def run_maketable_html(self, columns):
        return tableashtml.maketablehtml(columns)


class MDCode(MDBlock):
    """MD code block.

    Attributes
    ----------
    text : str
        Content of the block (one or more pars).

    """

    NAME = 'Code'

    VIEW = ''

    SPEC = """
    - May contain several paragraphs.
    - Must start and end with three backticks.
    - Code language — `LANG` — is fetched from the first line.
    
    Code blocks can represent
    
    - Code snippets.
    - Text snippets.

    <i>Code snippets</i>

    - Dumped to HTML as `&lt;pre>&lt;code>` pair.
    - CSS class `language-LANG` is assigned to `&lt;code>`.
    - `LANG` can be `python|c`.

    <i>Text snippets</i>
    
    - Dumped to HTML as `&lt;pre>` tag.
    - Assigned CSS class is `LANG`.

    """

    CODES = (
        'python', 'c'
    )

    def make_html(self) -> str:

        lang, body = self.parse_block()

        res = self.dump_to_pre_code_if_code(body, lang)

        if res is not None:
            return res

        return self.dump_to_pre_otherwise(body, cssclass=lang)

    def parse_block(self):

        text = self.text

        lang = self.get_lang(text)
        body = self.get_body(text)

        return lang, body

    def get_lang(self, text) -> str:
        firstline, *_ = text.partition('\n')
        return firstline.strip('` ')

    def get_body(self, text) -> str:

        text = self.cut_fringes(text)
        text = self.dedent_text(text)
        text = self.escape_html(text)

        return text

    def cut_fringes(self, text) -> str:
        return '\n'.join(
            text.splitlines()[1:-1]
        )

    def dedent_text(self, text):
        return textwrap.dedent(text)

    def dump_to_pre_code_if_code(self, body, lang):

        if not lang:
            return None

        if lang not in self.CODES:
            return None

        title = lang.title()
        label = f'<span class="lang-name">{title}</span>'
        code = f'<code class="language-{lang}">{body}</code>'

        return f'<pre>{label}{code}</pre>'

    def dump_to_pre_otherwise(self, body, cssclass=None):
        cssclass = self.set_css_class(cssclass)
        return f'<pre class="{cssclass}">{body}</pre>'

    def set_css_class(self, cssclass):
        return cssclass or 'docstring'


class DocBlock:
    """Documents a single block.
    """

    VIEWTEMP = '\n\n'.join(
        ['<i>Example</i>', '```text\n{}\n```']
    )

    SPECTEMP = '\n\n'.join(
        ['<i>Specification</i>', '{}']
    )

    def doc_block(self, block):

        data = self.take_data(block)
        text = self.make_text(data)

        return text

    def make_text(self, data):

        name, view, spec = data

        title = self.dump_title(name)
        view = self.dump_view(view)
        spec = self.dump_spec(spec)

        return self.assemble(title, view, spec)

    def dump_title(self, name):
        return f'## {name}'

    def dump_view(self, view) -> str:
        if not view:
            return ''

        if view.startswith('```'):
            view = textwrap.indent(view, prefix=' ')

        return self.VIEWTEMP.format(view)

    def dump_spec(self, spec) -> str:
        if not spec:
            return ''
        return self.SPECTEMP.format(spec)

    def take_data(self, block) -> list:

        name = self.fetch_name(block)
        view = self.fetch_view(block)
        spec = self.fetch_spec(block)

        return name, view, spec

    def fetch_name(self, block) -> str:
        return block.NAME

    def fetch_view(self, block) -> str:
        return textwrap.dedent(block.VIEW).strip()

    def fetch_spec(self, block) -> str:
        return textwrap.dedent(block.SPEC).strip()

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )


class Docser:
    """Creates documentation of blocks.
    """

    def docblocks(self) -> list[str]:

        blocks = self.fetch_blocks()

        blocklist = self.make_blocklist(blocks)
        blockdocs = self.make_blockdocs(blocks)

        return [
            blocklist, blockdocs
        ]

    def make_blocklist(self, blocks):

        items = [
            '- ' + self.asmdlink(block.NAME) for block in blocks
        ]

        return '\n'.join(items)

    def make_blockdocs(self, blocks):

        docser = DocBlock()

        return '\n\n'.join(
            map(docser.doc_block, blocks)
        )

    def fetch_blocks(self) -> list:
        return [
            obj for obj in globals().values() if self.is_block(obj)
        ]

    def asmdlink(self, text):

        name = text

        path = '-'.join(
            text.casefold().split()
        )

        return f'[{name}](#{path})'

    def is_block(self, obj):
        if not hasattr(obj, 'NAME'):
            return False
        if not obj.NAME:
            return False
        return True


BLOCKSLIST, BLOCKDOCS = Docser().docblocks()
