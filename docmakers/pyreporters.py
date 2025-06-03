# -*- coding: utf-8 -*-
"""Generates inspection reports on python scripts.
"""

import os
import textwrap
from . import utils
from ..docpage import pagemaker
from ..inspect import pyscripts
from ..inspect import pyoutline
from ..utils import texttrees, treeashtml

__all__ = [
    'docpackage', 'docscript'
]


apiobj = utils.apiobj


@apiobj
def docpackage(pkgpath, docpath, mode, maxdepth=None) -> None:
    """Creates an overview of a python package (static analysis).

    Parameters
    ----------
    pkgpath : str
        Path to the package directory.
    docpath : str
        Path where to place the output files.
    mode : str
        Specifies the output format — "html" or "md".
    maxdepth : int = None
        Maximum depth of nested subpackages.
        If None, all subpackages are included.

    """

    pkgpath = utils.check_srcdir(pkgpath)
    docpath = utils.check_docdir(docpath)

    doc_maker = get_docmaker_by_mode(mode)()

    doc_maker.docpkg(
        pkgpath=pkgpath, docpath=docpath, maxdepth=maxdepth
    )


def get_docmaker_by_mode(mode):

    mode = check_mode(mode)

    return globals().get(
        'PyPkg' + mode.upper()
    )


@apiobj
def docscript(filepath, docpath, mode) -> None:
    """Creates a report on a python script (static analysis).

    Parameters
    ----------
    filepath : str
        Path to the python script.
    docpath : str
        Path where to place the output files.
    mode : str
        Specifies the output format — <i>"html"</i> or <i>"md"</i>.

    """

    filepath = utils.check_srcfile(filepath)
    docpath = utils.check_docdir(docpath)

    name = os.path.basename(filepath).removesuffix('.py')
    content = utils.read_file(filepath)

    script = pyscripts.ScriptRecord(name, content)

    dumper = get_dumper_by_mode(mode)
    dumper(script, docpath)


def get_dumper_by_mode(mode):

    mode = check_mode(mode)

    return globals().get(
        f'dump_script_{mode}'
    )


def dump_script_md(script, docpath):

    filepath = os.path.join(
        docpath, script.name + '.md'
    )

    script.dumpreport(filepath)


def dump_script_html(script, docpath):

    filepath = os.path.join(
        docpath, script.name + '.html'
    )

    script.dumpdocpage(filepath)

    settings = pagemaker.PageParamsJS()
    settings.pagelogo = pagemaker.getlogo()

    pagemaker.dumpstatic(docpath, settings)


def check_mode(mode):

    WrongDocModeError = DocModeError

    if mode not in ['md', 'html']:
        raise WrongDocModeError(
            f'mode must be either "md" or "html", not {mode}'
        )

    return mode


def docpydir_html(dirpath, docpath, hostname='') -> str:
    """Documents a folder with python scripts (HTML format).

    Parameters
    ----------
    dirpath : str
        Path to the folder.
    docpath : str
        Path to the documentation.
    hostname : str
        Prefix for all docpage names.

    Returns
    -------
    str
        Local TOC as an MD list.

    """
    doc_maker = PyDirHTML()
    return doc_maker.docdir(dirpath, docpath, hostname)


def docpydir_md(dirpath, docpath, hostname=''):
    """Documents a folder with python scripts (MD format).

    Parameters
    ----------
    dirpath : str
        Path to the folder.
    docpath : str
        Path to the documentation.
    hostname : str
        Prefix for all report names.

    """
    doc_maker = PyDirMD()
    return doc_maker.docdir(dirpath, docpath, hostname)


class PyPkgDocs:
    """Docs generator for python packages (base class).
    """

    def __init__(self):

        self._pkgpath = None
        self._pkgname = None
        self._docpath = None

        self._maxdepth = None
        self._hostname = None
        self._level = None
        self._toc = None

    def set_locals(self, pkgpath, docpath, maxdepth):

        self._pkgpath = pkgpath
        self._pkgname = os.path.basename(pkgpath)
        self._docpath = docpath
        self._maxdepth = maxdepth

    def get_nested_folders(self, dirpath) -> list[str]:
        """Returns paths to subpackages in a given directory.
        """

        def is_eligigble_folder(name):
            if '.' in name:
                return False
            if name.startswith('_'):
                return False
            return True

        foldernames = list(
            filter(is_eligigble_folder, os.listdir(dirpath))
        )

        paths = [
            os.path.join(dirpath, name) for name in foldernames
        ]

        return list(
            filter(self.is_package, paths)
        )

    def is_package(self, dirpath):

        if not os.path.isdir(dirpath):
            return False

        # At least one python script.
        for filename in os.listdir(dirpath):
            if filename.endswith('.py'):
                return True

        return False


class PyPkgHTML(PyPkgDocs):
    """Documents a python package (HTML format).
    """

    def docpkg(self, pkgpath, docpath, maxdepth=2):

        preprocessor = self.set_locals
        preprocessor(pkgpath, docpath, maxdepth)

        tocastext = self.makehtml(pkgpath)
        self.dumpstatic(tocastext)

    def makehtml(self, pkgpath):

        self._level = 0

        self._toc = []
        self._hostname = []

        self.walk_to_make_doc(pkgpath)

        toc = '\n'.join(self._toc)

        list.clear(self._hostname)
        list.clear(self._toc)

        self._level = None
        return toc

    def walk_to_make_doc(self, dirpath):

        dirtoc = self.run_docpydir_html(
            dirpath, hostname='.'.join(self._hostname)
        )

        self.add_folder_to_toc(dirtoc)

        if self._level == self._maxdepth:
            return

        list.append(
            self._hostname, os.path.basename(dirpath)
        )

        subpkgs = self.get_nested_folders(dirpath)

        self._level += 1

        for pkgpath in subpkgs:
            self.walk_to_make_doc(pkgpath)

        self._level -= 1

        list.pop(
            self._hostname
        )

    def run_docpydir_html(self, dirpath, hostname):

        dirtoc = docpydir_html(
            dirpath, self._docpath, hostname=hostname
        )

        return dirtoc

    def add_folder_to_toc(self, dirtoc):

        tocentry = textwrap.indent(
            dirtoc, prefix=chr(32)*self._level
        )

        list.append(
            self._toc, tocentry
        )

    def set_logo(self):
        return pagemaker.getlogo()

    def set_homepage(self):
        """Returns the filename of the homepage.
        """

        pkgpage = self._pkgname + '.html'

        # No homepage.
        if pkgpage not in os.listdir(self._docpath):
            return ''

        return self.make_index_page()

    def set_contents(self, tocastext) -> str:
        root = texttrees.maketree(tocastext)
        return treeashtml.dumptree_html(root)

    def dumpstatic(self, tocastext):

        settings = pagemaker.PageParamsJS()

        settings.pagelogo = self.set_logo()
        settings.homepage = self.set_homepage()
        settings.contents = self.set_contents(tocastext)

        pagemaker.dumpstatic(
            self._docpath, settings, highlights=False
        )

    def make_index_page(self) -> str:
        """Makes the index page and returns its filename.
        """

        pkgpage = self._pkgname + '.html'

        script = f'<script>window.location="{pkgpage}"</script>'
        page = f'<!DOCTYPE html><html><body>{script}</body></html>'

        indexpath = os.path.join(
            self._docpath, 'index.html'
        )

        with open(indexpath, encoding='utf-8', mode='w') as file:
            file.write(page)

        return 'index.html'


class PyPkgMD(PyPkgDocs):
    """Documents a python package (MD format).
    """

    def docpkg(self, pkgpath, docpath, maxdepth=2):

        preprocessor = self.set_locals
        preprocessor(pkgpath, docpath, maxdepth)

        self._level = 0
        self._hostname = []

        self.walk_to_make_doc(self._pkgpath)

        list.clear(self._hostname)
        self._level = None

    def walk_to_make_doc(self, dirpath):

        self.run_docpydir_md(
            dirpath, hostname='.'.join(self._hostname)
        )

        if self._level == self._maxdepth:
            return

        list.append(
            self._hostname, os.path.basename(dirpath)
        )

        subpkgs = self.get_nested_folders(dirpath)

        self._level += 1

        for pkgpath in subpkgs:
            self.walk_to_make_doc(pkgpath)

        self._level -= 1

        list.pop(
            self._hostname
        )

    def run_docpydir_md(self, dirpath, hostname):
        docpydir_md(
            dirpath, self._docpath, hostname=hostname
        )


class PyDirDocs:
    """Docs generator for dirs with python scripts (base class).
    """

    FILEEXT = ''

    def __init__(self):

        self._dirpath = None
        self._docpath = None
        self._dirname = None
        self._hostname = None
        self._toc = None

    def set_locals(self, dirpath, docpath, hostname):

        self._dirpath = dirpath
        self._docpath = docpath
        self._dirname = os.path.basename(dirpath)

        self._hostname = '.'.join(
            filter(len, [hostname, self._dirname])
        )

        self._toc = []

    def docdir(self, dirpath, docpath, hostname) -> str | None:

        preprocessor = self.set_locals
        preprocessor(dirpath, docpath, hostname)

        scripts = self.getscripts()

        self.makeoutline(scripts)
        self.docscripts(scripts)

        if self._toc is None:
            return None
        return '\n'.join(self._toc)

    def makeoutline(self, _):
        pass

    def getscripts(self):
        return pyscripts.getscripts(self._dirpath)

    def docscripts(self, scripts):
        for script in scripts.getscripts():
            self.docscript(script)

    def docscript(self, _):
        pass

    def get_outline_filename(self):
        return '.'.join(
            [self._hostname, self.FILEEXT]
        )

    def get_script_filename(self, script):
        return '.'.join(
            [self._hostname, script.name, self.FILEEXT]
        )

    def get_base_filename(self, filename):
        basename, _ = os.path.splitext(filename)
        return basename.split('.').pop()


class PyDirHTML(PyDirDocs):
    """Documents a folder with python scripts (HTML format).
    """

    FILEEXT = 'html'

    def makeoutline(self, scripts):

        docpage = self.make_outline_html(scripts)
        self.save_outline_html(docpage)
        self.add_outline_to_toc()

    def make_outline_html(self, scripts) -> str:

        outline = pyoutline.makeoutline(scripts)

        settings = pagemaker.PageParamsHTML()

        settings.webtitle = self._hostname
        settings.doctitle = self._dirname

        docpage = pagemaker.makedocpage(
            sourcemd=outline, settings=settings
        )

        return docpage

    def save_outline_html(self, docpage):

        filename = self.get_outline_filename()

        filepath = os.path.join(
            self._docpath, filename
        )

        with open(filepath, encoding='utf-8', mode='w') as file:
            file.write(docpage)

    def docscript(self, script):
        self.dump_script_html(script)
        self.add_script_to_toc(script)

    def dump_script_html(self, script):

        filename = self.get_script_filename(script)

        filepath = os.path.join(
            self._docpath, filename
        )

        script.dumpdocpage(filepath)

    def add_outline_to_toc(self):

        outline_linker = self.make_link_to_outline

        list.append(
            self._toc, outline_linker()
        )

    def add_script_to_toc(self, script):

        linker = self.make_link_to_script

        list.append(
            self._toc, linker(script)
        )

    # Utils

    def make_link_to_outline(self):

        getfilename = self.get_outline_filename
        getbasename = self.get_base_filename

        filename = getfilename()
        basename = getbasename(filename)

        return f'- <a href="{filename}">{basename}</a>'

    def make_link_to_script(self, script):

        getfilename = self.get_script_filename
        getbasename = self.get_base_filename

        filename = getfilename(script)
        basename = getbasename(filename)

        return f' - <a href="{filename}">{basename}</a>'


class PyDirMD(PyDirDocs):
    """Documents a folder with python scripts (MD format).
    """

    FILEEXT = 'md'

    def makeoutline(self, scripts):
        self.dump_outline_md(scripts)

    def docscript(self, script):
        self.dump_script_md(script)

    def dump_outline_md(self, scripts):

        outline = pyoutline.makeoutline(scripts)

        filename = self.get_outline_filename()

        filepath = os.path.join(
            self._docpath, filename
        )

        with open(filepath, encoding='utf-8', mode='w') as file:
            file.write(outline)

    def dump_script_md(self, script):

        filename = self.get_script_filename(script)

        filepath = os.path.join(
            self._docpath, filename
        )

        script.dumpreport(filepath)


class DocModeError(Exception):
    """Raised when a wrong report format is passed.
    """
