# -*- coding: utf-8 -*-
"""Creates HTML docpages from MD files.
"""

import os
from . import templates
from .textmd import makehtml

__all__ = [
    'makedocpage', 'dumpstatic'
]

PageParamsJS = templates.PageParamsJS
PageParamsHTML = templates.PageParamsHTML


def apiobj(obj):
    obj.__module__ = 'docspyer.docpage'
    return obj


@apiobj
def makedocpage(sourcemd, settings=None):
    """Generates an HTML docpage from an MD source file.

    Parameters
    ----------
    sourcemd : str
        Content of the docpage in MD.
    settings : PageParamsHTML
        Settings of a docpage (a).

    Returns
    -------
    str
        The resulting HTML page.

    Notes
    -----

    (a) — Replaced by `PageParamsHTML()`, if None.

    """
    page_maker = DocPageMaker()
    return page_maker.make_page(sourcemd, settings)


@apiobj
def dumpstatic(dirpath, settings=None, highlights=False):
    """Dumps static JS/CSS files to the specified folder.

    Parameters
    ----------
    dirpath : str
        Path where to dump the files.
    settings : PageParamsJS
        Static docpage parameters (a).
    highlights : bool
        Code highlighting is activated, if True (b).

    Notes
    -----

    (a) — Replaced by `PageParamsJS()`, if None.

    (b) — Additional static files are copied.

    """

    dumper = StaticFilesDumper()
    settings = settings or PageParamsJS()

    dumper.dump_static_files(
        dirpath, settings, highlights
    )


def getlogo() -> str:

    path = os.path.join(
        templates.TEMPLATESPATH, 'logo.html'
    )

    with open(path, encoding='utf-8') as file:
        return file.read()


class DocPageMaker:
    """Generates an HTML docpage from an MD source file.
    """

    def __init__(self):
        self.set_page_template()

    def set_page_template(self):
        self.pagetemplate = templates.DocPageHTML()

    def make_page(self, sourcemd, settings):

        dochtml = self.convert_source(sourcemd)

        if settings is None:
            settings = PageParamsHTML()

        settings.localtoc = dochtml.toc
        settings.pagetext = dochtml.text

        docpage = self.render_docpage(settings)
        return docpage

    def convert_source(self, sourcemd):
        return self.run_textmd_makehtml(sourcemd)

    def run_textmd_makehtml(self, sourcemd):
        return makehtml.makedochtml(sourcemd)

    def render_docpage(self, settings):
        return self.pagetemplate.getpage(settings)


class StaticFilesDumper:
    """Dumps static JS/CSS files for an HTML docpage.
    """

    def __init__(self):
        self.set_templates()

    def set_templates(self):
        self.docpage_js = templates.DocPageJS()
        self.docpage_css = templates.DocPageCSS()
        self.highlights_js = templates.HighlightsJS()
        self.highlights_css = templates.HighlightsCSS()

    def dump_static_files(self, dirpath, settings, highlights):

        self.dump_docpage_files(dirpath, settings)
        self.dump_highlights_if_opted(dirpath, highlights)

    def dump_docpage_files(self, dirpath, settings):
        self.dump_docpage_js(dirpath, settings)
        self.dump_docpage_css(dirpath)

    def dump_docpage_js(self, dirpath, settings):

        docpage_js = FileToDump(
            name=self.docpage_js.sourcename,
            source=self.docpage_js.getpage(settings)
        )

        docpage_js.dump(dirpath)

    def dump_docpage_css(self, dirpath):

        docpage_css = FileToDump(
            name=self.docpage_css.sourcename,
            source=self.docpage_css.getsource()
        )

        docpage_css.dump(dirpath)

    def dump_highlights_if_opted(self, dirpath, highlights):

        if highlights is False:
            return

        file_js = FileToDump(
            name=self.highlights_js.sourcename,
            source=self.highlights_js.getsource()
        )

        file_css = FileToDump(
            name=self.highlights_css.sourcename,
            source=self.highlights_css.getsource()
        )

        file_js.dump(dirpath)
        file_css.dump(dirpath)


class FileToDump:

    TEMPLATESPATH = templates.TEMPLATESPATH

    def __init__(self, name, source):
        self.name = name
        self.source = source

    def dump(self, dirpath):

        self.check_is_not_template(
            dirpath, self.name
        )

        path = os.path.join(dirpath, self.name)

        with open(path, encoding='utf-8',  mode='w') as file:
            file.write(self.source)

    def check_is_not_template(self, dirpath, name):

        if name not in os.listdir(self.TEMPLATESPATH):
            return

        if name not in os.listdir(dirpath):
            return

        filepath = os.path.join(dirpath, name)
        templatepath = os.path.join(self.TEMPLATESPATH, name)

        is_template = os.path.samefile(
            filepath, templatepath
        )

        if not is_template:
            return

        raise ValueError(
            f"check the path, writing to the template '{name}' attempted"
        )
