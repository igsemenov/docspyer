# -*- coding: utf-8 -*-
"""Placeholders in mutable templates.

Mutable templates are:

- 'docpage.htm'
- 'docpage.js'

"""

import re
import textwrap


class Anchor:
    """Base class for anchors.

    Attributes
    ----------
    text : str
        Anchor text.

    """

    text = None

    def __init__(self):
        self._indent = None
        self._lineno = None
        self.set_text()

    def set_text(self):
        self.text = self.__class__.text

    def replace_anchor(self, source, newdata=None):
        """Replaces the anchor in a source document.

        Parameters
        ----------
        source : str
            Source document that contains the anchor.
        newdata : str
            Data for making the anchor substitute.

        Returns
        -------
        str
            The new source document.

        """

        self.set_internal_vars(source)

        newval = self.make_substitute(newdata)
        source = self.put_substitute(source, newval)

        self._lineno = None
        self._indent = None

        return source

    def set_internal_vars(self, source):
        self._lineno = self.find_line_with_anchor(source)
        self._indent = self.get_anchor_indent(source)

    def remove_anchor(self, source) -> str:
        """Removes anchor from the source document.

        Returns
        -------
        str
            The new source document.

        """

        self._lineno = self.find_line_with_anchor(source)

        source = self.remove_line_with_anchor(source)

        self._lineno = None
        return source

    def make_substitute(self, newdata=None) -> str:
        """TBD
        """
        return self.text.replace('STUB', newdata)

    def put_substitute(self, source, substitute) -> str:
        """TBD
        """
        return self.replace_anchor_in_line(source, substitute)

    # Utils

    def replace_anchor_in_line(self, source, substitue) -> str:

        index = self._lineno
        lines = source.splitlines(True)

        lines[index] = lines[index].replace(self.text, substitue)

        return ''.join(lines)

    def replace_line_where_anchor(self, source, substitute) -> str:

        index = self._lineno
        lines = source.splitlines(True)

        lines[index] = substitute.rstrip('\n') + '\n'

        return ''.join(lines)

    def remove_line_with_anchor(self, source) -> str:

        index = self._lineno
        lines = source.splitlines(True)

        lines.pop(index)

        return ''.join(lines)

    def get_anchor_indent(self, source) -> int:

        index = self._lineno
        lines = source.splitlines(True)

        line = lines[index]

        return len(line) - len(str.lstrip(line))

    def find_line_with_anchor(self, source) -> int | None:

        lines = source.splitlines(True)

        for index, line in enumerate(lines):
            if line.strip() == self.text:
                return index

        return None


class Header(Anchor):
    """Headers in 'docpage.html'.

    Headers are:

    - Title of the webpage (webtitle).
    - Title of the document (doctitle).
    - Annotation of the document (annotation).

    """

    re_header = '(Docpage|Title|Annotation)'

    def make_substitute(self, newdata=None):

        if newdata is None:
            return self.text

        return re.sub(
            self.re_header, newdata, self.text
        )

    def put_substitute(self, source, substitute) -> str:
        return self.replace_anchor_in_line(source, substitute)


class Webtitle(Header):
    text = '<title>Docpage</title>'


class Doctitle(Header):
    text = '<h1 id="title-box__title">Title</h1>'


class Annotation(Header):
    text = '<h2 id="title-box__annotation">Annotation</h2>'


class PageContent(Anchor):
    """Content items in 'docpage.html'.

    Content items are:

    - Local table of contents (localtoc).
    - Content of the document (pagetext).

    """

    def make_substitute(self, newdata=None):
        if newdata is None:
            return self.text
        return newdata

    def put_substitute(self, source, substitute) -> str:
        handler = self.assign_handler()
        return handler(source, substitute)

    def assign_handler(self):
        return self.replace_anchor_in_line


class LocalTOC(PageContent):

    text = '<!--local-toc-->'

    def make_substitute(self, newdata=None):

        if newdata is None:
            return self.text

        return textwrap.indent(
            newdata, prefix=self._indent*chr(32)
        )

    def assign_handler(self):
        return self.replace_line_where_anchor


class PageText(PageContent):

    text = '<!--page-text-->'


class PageSettings(Anchor):
    """Docpage settings in 'docpage.js'.

    Page settings are:

    - Logo of the webpage (pagelogo).
    - Global table of contents (contents).
    - Path linked to the homepage (homepage).

    """

    def make_substitute(self, newdata=None):

        if newdata is None:
            return self.text

        return str.replace(
            self.text, '= null;', f'= `{newdata}`;'
        )

    def put_substitute(self, source, substitute) -> str:
        return self.replace_anchor_in_line(source, substitute)


class PageLogo(PageSettings):
    text = 'docPage.pagelogo = null;'


class GlobalTOC(PageSettings):
    text = 'docPage.contents = null;'


class HomePage(PageSettings):
    text = 'docPage.homepage = null;'


class Highlight(Anchor):
    """Settings for code highlighting in 'docpage.html'.

    Settings are:

    - Static links to JS/CSS files.
    - Function call in the body-script.

    """

    repl = None

    def make_substitute(self, newdata=None):
        newdata = self.repl
        return newdata

    def put_substitute(self, source, substitute) -> str:
        return self.replace_anchor_in_line(source, substitute)


class HighlightJS(Highlight):
    text = '<!--highlights-js-->'
    repl = '<script src="highlight.min.js"></script>'


class HighlightCSS(Highlight):
    text = '<!--highlights-css-->'
    repl = '<link rel="stylesheet" href="default.min.css">'


class HighlightFunc(Highlight):
    text = '/*highlights-func*/'
    repl = 'hljs.highlightAll();'
