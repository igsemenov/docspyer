# -*- coding: utf-8 -*-
"""Template files used to create docpages.
"""

import os
from . import anchors

__all__ = [
    'PageParamsJS', 'PageParamsHTML'
]


def apiobj(obj):
    obj.__module__ = 'docspyer.docpage'
    return obj


def get_path_to_templates() -> str:
    """Returns the path to the template folder.

    - Templates folder is named 'templates'.
    - Templates folder is placed next to 'templates.py'.

    """
    return __file__.removesuffix('.py')


TEMPLATESPATH = get_path_to_templates()


class Template:
    """Base class for template files.
    """

    sourcename = None

    def getsourcename(self) -> str:
        return self.sourcename

    def getsource(self):
        name = self.getsourcename()
        path = os.path.join(TEMPLATESPATH, name)
        with open(path, encoding='utf-8') as file:
            return file.read()


class MutableDoc(Template):
    """Base class for mutable templates

    - Mutable templates contain expressions that can be edited (anchors).

    """


class DocPageHTML(MutableDoc):

    sourcename = 'docpage.html'

    def __init__(self):

        self.settings = None

        self.anchors_headers = None
        self.anchors_content = None
        self.anchors_hljs = None

        self.set_anchors()

    def set_anchors(self):
        self.set_headers()
        self.set_content()
        self.set_highlights()

    def set_headers(self):

        self.anchors_headers = {
            'webtitle': anchors.Webtitle(),
            'doctitle': anchors.Doctitle(),
            'annotation': anchors.Annotation()
        }

    def set_content(self):

        self.anchors_content = {
            'localtoc': anchors.LocalTOC(),
            'pagetext': anchors.PageText()
        }

    def set_highlights(self):

        self.anchors_hljs = {
            'js': anchors.HighlightJS(),
            'css': anchors.HighlightCSS(),
            'func': anchors.HighlightFunc(),
        }

    def getpage(self, settings=None) -> str:

        source = self.getsource()

        if settings is None:
            return source

        self.settings = settings

        source = self.handle_highlights(source)
        source = self.add_headers(source)
        source = self.add_content(source)

        return source

    def add_headers(self, temp):

        temp = self.anchors_headers['webtitle'].replace_anchor(
            temp, self.settings.webtitle
        )

        temp = self.anchors_headers['annotation'].replace_anchor(
            temp, self.settings.annotation
        )

        temp = self.anchors_headers['doctitle'].replace_anchor(
            temp, self.settings.doctitle
        )

        return temp

    def add_content(self, source):

        source = self.anchors_content['localtoc'].replace_anchor(
            source, self.settings.localtoc
        )

        source = self.anchors_content['pagetext'].replace_anchor(
            source, self.settings.pagetext
        )

        return source

    def handle_highlights(self, source):

        highlights = self.settings.highlights

        if highlights is True:
            return self.add_highlights_if_true(source)

        if highlights is False:
            return self.remove_highlights_if_false(source)

        return source

    def add_highlights_if_true(self, source):

        anchors_hljs = dict.values(self.anchors_hljs)

        for anchor in anchors_hljs:
            source = anchor.replace_anchor(source)

        return source

    def remove_highlights_if_false(self, source):

        anchors_hljs = dict.values(self.anchors_hljs)

        for anchor in anchors_hljs:
            source = anchor.remove_anchor(source)

        return source


class DocPageJS(MutableDoc):

    sourcename = 'docpage.js'

    def __init__(self):

        self.anchors = None
        self.settings = None

        self.set_anchors()

    def set_anchors(self):

        self.anchors = {
            'pagelogo': anchors.PageLogo(),
            'contents': anchors.GlobalTOC(),
            'homepage': anchors.HomePage()
        }

    def getpage(self, settings=None) -> str:

        source = self.getsource()

        if settings is None:
            return source

        self.settings = settings

        source = self.add_anchors(source)
        return source

    def add_anchors(self, source):

        source = self.anchors['pagelogo'].replace_anchor(
            source, self.settings.pagelogo
        )

        source = self.anchors['contents'].replace_anchor(
            source, self.settings.contents
        )

        source = self.anchors['homepage'].replace_anchor(
            source, self.settings.homepage
        )

        return source


class DocPageCSS(Template):
    sourcename = 'docpage.css'


class HighlightsJS(Template):
    sourcename = 'highlight.min.js'


class HighlightsCSS(Template):
    sourcename = 'default.min.css'


@apiobj
class PageParamsHTML:
    """Settings added to the template file `docpage.html`.

    Attributes
    ----------
    webtitle : str = ''
        Title of the webpage.
    doctitle : str = ''
        Title of the document.
    annotation : str = ''
        Annotation of the document.
    localtoc : str = ''
        Local TOC as an HTML list inside a paragraph.
    pagetext : str = ''
        Content of a docpage as text in HTML.
    highilights : bool = False
       Code highlighting is activated, if True (a).

    Notes
    -----

    (a) — Links to static files are added,
          call of JS based highlighter is included.

    """

    def __init__(self):

        self.webtitle = ''
        self.doctitle = ''
        self.annotation = ''
        self.localtoc = ''
        self.pagetext = ''
        self.highlights = False


@apiobj
class PageParamsJS:
    """Settings added to the template file `docpage.js`.

    Attributes
    ----------
    pagelogo : str = ''
        Page logo as an SVG or HTML tag.
    contents : str = ''
        Global TOC as an HTML list inside a paragraph.
    homepage : str = ''
        Path to the homepage.

    """

    def __init__(self):

        self.pagelogo = ''
        self.contents = ''
        self.homepage = ''
