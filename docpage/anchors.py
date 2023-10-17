# -*- coding: utf-8 -*-
"""Text chunks that are replaced in templates.

- Anchors are present in mutable templates only.
- Anchors take templates from the outside at runtime.
- Anchors replace themself in templates and returns the result.

Public methods:

    Anchor().replace_anchor(temp, data=None) → str
    Anchor().remove_anchor(temp) → str

Mutable templates:

- 'docpage.js'
- 'docpage.htm'

Static templates:

- 'docpage.css'
- 'default.min.css'
- 'highlight.min.js'

"""

import re
import textwrap


def todefine(obj):
    return obj


class Anchor:
    """Base class for anchors.

    Attributes
    ----------
    TEXT : str
        Anchor text.

    """

    TEXT = ''

    def __init__(self):
        self._indent = None
        self._lineno = None

    def replace_anchor(self, temp, data=None):
        """Replaces the anchor in a template.

        Parameters
        ----------
        temp : str
            Template that contains the anchor.
        data : str
            Data to make the anchor replacement.

        Returns
        -------
        str
            The resulting document.

        """

        self.find_anchor(temp)

        repl = self.set_replacement(data)
        resdoc = self.put_replacement(temp, repl)

        self._lineno = None
        self._indent = None

        return resdoc

    def remove_anchor(self, temp) -> str:
        """Removes the anchor from a template.

        Returns
        -------
        str
            The resulting document.

        """

        lineno = self.find_anchor_line(temp)
        resdoc = self.remove_anchor_line(temp, lineno)

        return resdoc

    def find_anchor(self, temp):
        self._lineno = self.find_anchor_line(temp)
        self._indent = self.find_anchor_indent(temp)

    @todefine
    def set_replacement(self, data=None) -> str:
        """Makes the anchor replacement.
        """

    @todefine
    def put_replacement(self, temp, repl) -> str:
        """Inserts the anchor replacement into the template.
        """

    def replace_anchor_in_line(self, temp, repl) -> str:

        lines = temp.splitlines(True)

        index = self._lineno
        lines[index] = lines[index].replace(self.TEXT, repl)

        return ''.join(lines)

    def replace_line_where_anchor(self, temp, repl) -> str:

        lines = temp.splitlines(True)

        index = self._lineno
        lines[index] = repl.rstrip('\n') + '\n'

        return ''.join(lines)

    def remove_anchor_line(self, temp, lineno) -> str:

        lines = temp.splitlines(True)
        lines.pop(lineno)

        return ''.join(lines)

    def find_anchor_indent(self, temp) -> int:

        lines = temp.splitlines(True)

        index = self._lineno
        line = lines[index]

        return len(line) - len(str.lstrip(line))

    def find_anchor_line(self, temp) -> int | None:

        lines = temp.splitlines(True)

        for index, line in enumerate(lines):
            if line.strip() == self.TEXT:
                return index

        return None


class Header(Anchor):
    """Headers in 'docpage.html'.

    Headers are:

    - Title of the webpage (webtitle).
    - Title of the document (doctitle).
    - Annotation of the document (annotation).

    """

    RE_HEADER = '(Docpage|Title|Annotation)'

    def set_replacement(self, data=None):

        if data is None:
            return self.TEXT

        return self.re_sub_header_data_text(data)

    def put_replacement(self, temp, repl) -> str:
        return self.replace_anchor_in_line(temp, repl)

    def re_sub_header_data_text(self, data):
        return re.sub(
            self.RE_HEADER, data, self.TEXT
        )


class Webtitle(Header):
    TEXT = '<title>Docpage</title>'


class Doctitle(Header):
    TEXT = '<h1 id="title-box__title">Title</h1>'


class Annotation(Header):
    TEXT = '<h2 id="title-box__annotation">Annotation</h2>'


class PageContent(Anchor):
    """Content items in 'docpage.html'.

    Content items are:

    - Local table of contents (localtoc).
    - Content of the document (pagetext).

    """

    def set_replacement(self, data=None):
        if data is None:
            return self.TEXT
        return self.take_user_data_asis(data)

    def put_replacement(self, temp, repl) -> str:
        return self.replace_line_where_anchor(temp, repl)

    def take_user_data_asis(self, data):
        return data


class LocalTOC(PageContent):

    TEXT = '<!--local-toc-->'

    def take_user_data_asis(self, data):
        return textwrap.indent(
            data, prefix=self._indent*chr(32)
        )


class PageText(PageContent):

    TEXT = '<!--page-text-->'

    def take_user_data_asis(self, data):
        return data + '\n\n<hr>'


class PageSettings(Anchor):
    """Docpage settings in 'docpage.js'.

    Page settings are:

    - Logo of the webpage (pagelogo).
    - Global table of contents (contents).
    - Path linked to the homepage (homepage).

    """

    def set_replacement(self, data=None):

        if data is None:
            return self.TEXT

        return self.text_repl_eqnull_eqdata(data)

    def put_replacement(self, temp, repl) -> str:
        return self.replace_anchor_in_line(temp, repl)

    def text_repl_eqnull_eqdata(self, data):
        return str.replace(
            self.TEXT, '= null;', f'= `{data}`;'
        )


class PageLogo(PageSettings):
    TEXT = 'docPage.pagelogo = null;'


class GlobalTOC(PageSettings):
    TEXT = 'docPage.contents = null;'


class HomePage(PageSettings):
    TEXT = 'docPage.homepage = null;'


class Highlight(Anchor):
    """Settings for code highlighting in 'docpage.html'.

    Settings are:

    - Links to static JS/CSS files.
    - JS call in the body-script.

    """

    REPL = ''

    def set_replacement(self, data=None):
        return self.push_prescribed_repl()

    def put_replacement(self, temp, repl) -> str:
        return self.replace_anchor_in_line(temp, repl)

    def push_prescribed_repl(self):
        return self.REPL


class HighlightJS(Highlight):
    TEXT = '<!--highlights-js-->'
    REPL = '<script src="highlight.min.js"></script>'


class HighlightCSS(Highlight):
    TEXT = '<!--highlights-css-->'
    REPL = '<link rel="stylesheet" href="default.min.css">'


class HighlightFunc(Highlight):
    TEXT = '/*highlights-func*/'
    REPL = 'hljs.highlightAll();'
