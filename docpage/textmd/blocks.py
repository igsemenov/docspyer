# -*- coding: utf-8 -*-
"""Blocks of Markdown (MD) text.
"""

import re
import textwrap
from docspy.utils import texttrees
from docspy.utils import treeashtml
from docspy.utils import tableashtml
from . import emphase


class MDBlock:
    """Base class for MD blocks.
    """

    def __init__(self, text):
        self.text = text

    def get_text(self):
        return self.text

    def is_heading(self):
        return isinstance(self, MDHeading)

    def is_list(self):
        return isinstance(self, MDList)


class MDHeading(MDBlock):
    """One-line heading.

    Attributes
    ----------
    text : str
        Line with a heading.

    """

    def make_html(self) -> str:
        heading = self.make_html_heading()
        return self.add_toc_anchor_prefix(heading)

    def make_html_heading(self):
        level = self.get_level()
        content = self.get_content()
        return f'<h{level}>{content}</h{level}>'

    def add_toc_anchor_prefix(self, heading):
        return '<div class="toc-anchor"></div>' + heading

    def get_level(self) -> int:
        return str.count(self.text, '#')

    def get_content(self) -> str:
        return str.lstrip(self.text, '# ')


class MDHrule(MDBlock):
    """Horizontal rule.
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

    RE_HTML_BLOCK = '<(p|dl|svg)'

    def make_html(self) -> str:

        res = self.dump_unchanged_if_is_to_ignore()

        if res is not None:
            return res

        return self.dump_to_ptag_otherwise()

    def dump_unchanged_if_is_to_ignore(self):
        if self.is_to_ignore():
            return self.text
        return None

    def dump_to_ptag_otherwise(self):
        text = self.text
        text = self.emphasize(text)
        return '<p>' + text + '</p>'

    def emphasize(self, text):
        return emphase.edit_inline_md(text)

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
        if text.startswith("<!--") and text.endswith("-->"):
            return True
        return False


class MDList(MDBlock):
    """MD list.

    Attributes
    ----------
    text : str
        Paragraph with a list.

    """

    def make_html(self) -> str:
        root = self.convert_list_to_tree(self.text)
        return self.print_tree_in_html(root)

    def convert_list_to_tree(self, text_with_list):
        return self.run_maketree_from_texttrees(text_with_list)

    def print_tree_in_html(self, root) -> str:
        return treeashtml.dumptree_html(root)

    def run_maketree_from_texttrees(self, text_with_list):
        return texttrees.maketree(text_with_list)


class MDTable(MDBlock):
    """MD table.

    Attributes
    ----------
    text : str
        Paragraph with a table.

    """

    def make_html(self) -> str:
        columns = self.fetch_columns_from_text()
        return self.run_maketable_html(columns)

    def fetch_columns_from_text(self) -> list[list[str]]:
        rows = self.fetch_rows_from_text()
        rows = self.exclude_second_row(rows)
        return self.convert_rows_to_columns(rows)

    def exclude_second_row(self, rows):
        return [
            rows[0], *rows[2::]
        ]

    def fetch_rows_from_text(self) -> list[list[str]]:

        lines = str.splitlines(self.text)

        return [
            line.strip('|').split('|') for line in lines
        ]

    def convert_rows_to_columns(self, rows) -> list[list[str]]:

        def getcolumn(rows):
            return list(map(list.pop, rows))

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

    LANGS = (
        'python', 'c'
    )

    def make_html(self) -> str:

        text = self.get_content_from_body()
        lang = self.get_lang_from_first_line()

        res = self.dump_to_pre_code_if_lang(text, lang)
        if res is not None:
            return res

        return self.dump_to_pre_otherwise(text, classname=lang)

    def get_content_from_body(self) -> str:
        content = self.get_inner_lines()
        return self.dedent_resulting_text(content)

    def get_inner_lines(self) -> str:
        return '\n'.join(
            str.splitlines(self.text)[1:-1]
        )

    def dedent_resulting_text(self, text):
        return textwrap.dedent(text)

    def get_lang_from_first_line(self) -> str:
        firstline, _, _ = str.partition(self.text, '\n')
        language = firstline.strip('` ')
        return language

    def dump_to_pre_code_if_lang(self, text, lang):

        if not lang:
            return None

        if lang not in self.LANGS:
            return None

        langname = lang.title()
        label = f'<span class="lang-name">{langname}</span>'

        code = f'<code class="language-{lang}">{text}</code>'
        return f'<pre>{label}{code}</pre>'

    def dump_to_pre_otherwise(self, text, classname=None):

        if not classname:
            return f'<pre>{text}</pre>'

        return f'<pre class="{classname}">{text}</pre>'
