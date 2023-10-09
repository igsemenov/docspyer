# -*- coding: utf-8 -*-
"""Text chunks that are replaced in templates.

- Anchors are present in mutable templates only.
- Anchors replace themself in templates.
- The replacement is from user data.

Mutable templates:

- 'docpage.js'
- 'docpage.htm'

Static templates:

- 'docpage.css'
- 'default.min.css'
- 'highlight.min.js'

"""
from abc import ABC, abstractmethod
import re
import textwrap


class Anchor(ABC):
    """Base class for anchors.
    """

    TEXT = ''

    def replace_anchor(self, template, userdata=None):
        """Replaces the anchor in a template.

        Parameters
        ----------
        template : str
            Template that contains the anchor.
        userdata : str
            User data to make the replacement.

        Returns
        -------
        str
            The resulting document.

        """

        lineno, indent = self.find_anchor(template)

        anchor_repl = self.get_replacement(userdata, indent)
        newdocument = self.put_replacement(template, anchor_repl, lineno)

        return newdocument

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

        lineno = self.find_anchor_line(temp)
        indent = self.find_anchor_indent(temp, lineno)

        return lineno, indent

    @abstractmethod
    def get_replacement(self, data=None, indent=None):
        """Makes the anchor replacement.
        """

    @abstractmethod
    def put_replacement(self, temp, repl, lineno) -> str:
        """Inserts the anchor replacement into the template.
        """

    def replace_anchor_in_line(self, temp, repl, lineno):

        lines = temp.splitlines(True)
        lines[lineno] = lines[lineno].replace(self.TEXT, repl)

        return ''.join(lines)

    def replace_line_where_anchor(self, temp, repl, lineno):

        lines = temp.splitlines(True)
        lines[lineno] = repl.rstrip('\n') + '\n'

        return ''.join(lines)

    def remove_anchor_line(self, temp, lineno) -> str:

        lines = temp.splitlines(True)
        lines.pop(lineno)

        return ''.join(lines)

    def find_anchor_line(self, temp):

        lines = temp.splitlines(True)

        for index, line in enumerate(lines):
            if line.strip() == self.TEXT:
                return index

        return None

    def take_anchor_line(self, temp, lineno):
        return temp.splitlines(True).pop(lineno)

    def find_anchor_indent(self, temp, lineno):

        line = self.take_anchor_line(temp, lineno)
        data = self.find_indentation(line)

        return data

    def find_indentation(self, line):
        return len(line) - len(str.lstrip(line))


class Header(Anchor):
    """Headers in 'docpage.html'.

    Headers are:

    - Title of the webpage (webtitle).
    - Title of the document (doctitle).
    - Annotation of the document (annotation).

    """

    RE_HEADER = '(Docpage|Title|Annotation)'

    def get_replacement(self, data=None, indent=None):

        if data is None:
            return self.TEXT

        return self.put_user_data_to_header(data)

    def put_user_data_to_header(self, data):
        return re.sub(
            self.RE_HEADER, data, self.TEXT
        )

    def put_replacement(self, temp, repl, lineno):
        return self.replace_anchor_in_line(temp, repl, lineno)


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

    def get_replacement(self, data=None, indent=None):
        if data is None:
            return self.TEXT
        return self.take_user_data(data, indent)

    @abstractmethod
    def take_user_data(self, data, indent):
        """Returns user data probably indented.
        """

    def put_replacement(self, temp, repl, lineno):
        return self.replace_line_where_anchor(temp, repl, lineno)


class LocalTOC(PageContent):

    TEXT = '<!--local-toc-->'

    def take_user_data(self, data, indent):
        return textwrap.indent(
            data, prefix=indent*chr(32)
        )


class PageText(PageContent):

    TEXT = '<!--page-text-->'

    def take_user_data(self, data, indent):
        return indent * '' + data + '\n\n<hr>'


class PageSettings(Anchor):
    """Docpage settings in 'docpage.js'.

    Page settings are:

    - Logo of the webpage (pagelogo).
    - Global table of contents (contents).
    - Path linked to the homepage (homepage).

    """

    def get_replacement(self, data=None, indent=None):

        if data is None:
            return self.TEXT

        return self.insert_user_data(data)

    def insert_user_data(self, data):
        return str.replace(
            self.TEXT, '= null;', f'= `{data}`;'
        )

    def put_replacement(self, temp, repl, lineno):
        return self.replace_anchor_in_line(temp, repl, lineno)


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

    def get_replacement(self, data=None, indent=None):
        return self.push_prescribed_repl()

    def put_replacement(self, temp, repl, lineno):
        return self.replace_anchor_in_line(temp, repl, lineno)

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
