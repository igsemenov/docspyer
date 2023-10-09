# -*- coding: utf-8 -*-
"""Generates HTML documentation from MD source files.
"""

import os
import re
import json

from . import utils
from ..docpage import pagemaker
from ..docpage import textmd
from ..utils import treeashtml, texttrees

__all__ = [
    'docsource', 'builddocs', 'docsconfig'
]

apiobj = utils.apiobj
formatdoc = utils.formatdoc


@apiobj
def docsource(srcpath, docpath, codeblocks=False) -> None:
    """Converts an MD source file to an HTML page.

    Parameters
    ----------
    srcpath : str
        Path to the source file.
    docpath : str
        Path where to place the output files.
    codeblocks : bool
        Code highlighting is activated, if True.

    """

    srcpath = utils.check_srcfile(srcpath)
    docpath = utils.check_docdir(docpath)

    srcfile = SourceFile()
    srcfile = srcfile.set_file(srcpath)
    srcfile.dumpdocpage(docpath, codeblocks)

    pagemaker.dumpstatic(
        docpath, settings=None, highlights=codeblocks
    )


@apiobj
def builddocs(srcpath, docpath, config=None) -> None:
    """Assemble HTML documentation from MD source files.

    Parameters
    ----------
    srcpath : str
        Path to the source directory.
    docpath : str
        Path where to place the output files.
    config : dict
        Configuration parameters, see `docsconfig()`.
        If None, the default settings are used.

    """

    srcpath = utils.check_srcdir(srcpath)
    docpath = utils.check_docdir(docpath)

    doc_builder = DocsBuilder()

    doc_builder.build_docs(
        srcpath, docpath, config or {}
    )


def what_is_config() -> str:
    return "configuration parameters of the documentation builder"


@apiobj
@formatdoc(
    configparams=what_is_config()
)
def docsconfig() -> dict:
    """Returns a template for setting {configparams}.

    The template is a dictionary where:

    - The keys are the parameters names.
    - The values specify the default settings.

    Keys
    ----
    doclogo : str = ''
        Documentation logo as an SVG or HTML tag.
        The recommended size is 30-40px.
    codeblocks : bool = True 
        Code highlighting is activated, if True.
    swaplinks : bool = False
        If True, links to MD files are converted 
        to HTML ones across the source files.
    extracss : str = ''
        Custom CSS styles to include.
    extrajs : str = ''
        Custom JS code to include.

    """
    return {
        'doclogo': '',
        'codeblocks': True,
        'swaplinks': False,
        'extracss': '',
        'extrajs': ''
    }


class DocsBuilder:
    """Assembles HTML documentation from MD source files.
    """

    def __init__(self):

        self._srcdir = None
        self._docdir = None
        self._config = None

    def build_docs(self, srcdir, docdir, config):

        self._srcdir = srcdir
        self._docdir = docdir
        self._config = docsconfig() | config

        sources = self.get_sources()
        self.edit_sources(sources.files)

        self.doc_sources(sources.files)
        self.dump_static(sources.contents)

    def get_sources(self):
        return SourceFiles().set_sources(self._srcdir)

    def edit_sources(self, files):

        if self._config['swaplinks']:
            self.swaplinks(files)

    def doc_sources(self, files):
        for file in files.values():
            file.dumpdocpage(self._docdir)

    def dump_static(self, contents):

        settings = pagemaker.PageParamsJS()

        doclogo = self._config['doclogo']
        codeblocks = self._config['codeblocks']

        settings.pagelogo = doclogo
        settings.contents = contents
        settings.homepage = 'index.html'

        pagemaker.dumpstatic(
            self._docdir, settings=settings, highlights=codeblocks
        )

        self.add_extra_css_if_any()
        self.add_extra_js_if_any()

    def swaplinks(self, files):
        for file in files.values():
            file.swaplinks()

    def add_extra_css_if_any(self):
        getattr(self, 'add_extra_static')(mode='css')

    def add_extra_js_if_any(self):
        getattr(self, 'add_extra_static')(mode='js')

    def add_extra_static(self, mode):

        extracode = self._config['extra' + mode]

        if not extracode:
            return

        extracode = '/* Custom code */\n\n' + extracode

        filepath = os.path.join(
            self._docdir, 'docpage.' + mode
        )

        content = utils.read_file(filepath)
        content = content + '\n\n' + extracode

        utils.dump_file(filepath, content)


class SourceFiles:
    """Preprocessed source files.

    Attributes
    ----------
    files : dict
        Namespace of source files (name-to-object).
    contents : str
        Global TOC as an HTML list.

    """

    def __init__(self):
        self.files = None
        self.contents = None

    def set_sources(self, srcdir):

        name_to_file = self.get_sources(srcdir)

        indexfile = name_to_file.get('index')
        globaltoc = indexfile.toc

        self.set_files(name_to_file)
        self.set_contents(globaltoc)

        return self

    def set_files(self, name_to_file):
        setattr(self, 'files', name_to_file)

    def set_contents(self, globaltoc):
        setattr(self, 'contents', globaltoc)

    def get_sources(self, srcdir) -> dict:
        """Returns the namespace of source files (name-to-object).
        """

        def makefile(filepath):
            if filepath.endswith('index.md'):
                return IndexFile().set_file(filepath)
            return SourceFile().set_file(filepath)

        self.check_index_is_available(srcdir)

        pathsgetter = self.get_source_paths
        filepaths = pathsgetter(srcdir)

        files = list(
            map(makefile, filepaths)
        )

        return {
            file.name: file for file in files
        }

    def get_source_paths(self, srcdir) -> list[str]:
        """Returns paths to the source files.
        """

        def is_source(name):
            return name.endswith('.md')

        filenames = list(
            filter(is_source, os.listdir(srcdir))
        )

        return [
            os.path.join(srcdir, name) for name in filenames
        ]

    def check_index_is_available(self, srcdir):

        if 'index.md' in os.listdir(srcdir):
            return

        raise NoIndexFileError(
            f"no 'index.md' in the source directory: {srcdir}"
        )


class SourceFile:
    """A preprocessed source file.

    Attributes
    ----------
    name : str
        File name
    text : str
        File content (edited).
    meta : dict
        Settings for the pagemaker.

    """

    def __init__(self):

        self.name = None
        self.text = None
        self.meta = None

        self._filename = None

    def set_file(self, filepath):

        sourcemd = self.read_source(filepath)

        filename = os.path.basename(filepath).removesuffix('.md')
        self._filename = filename

        self.set_name(filename)
        self.set_text(sourcemd)
        self.set_meta(sourcemd)

        return self

    def set_name(self, filename):
        self.name = filename

    def set_text(self, sourcemd):
        self.text = sourcemd

    def set_meta(self, sourcemd):
        self.meta = self.extract_meta_if_any(sourcemd)
        self.text = self.remove_meta_from_text(sourcemd)

    def extract_meta_if_any(self, sourcemd) -> dict:

        par = self.fetch_first_par(sourcemd)

        if not self.is_par_comment(par):
            return {}

        content = par.strip('<!- >\n')

        if not self.is_with_json(content):
            return {}

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        raise FileMetaDataError(
            f"JSON metadata for '{self._filename}' cannot be parsed"
        )

    def remove_meta_from_text(self, text):

        par = self.fetch_first_par(text)
        par_is_meta = self.meta != {}

        return self.remove_par_if_meta(
            text, par, par_is_meta
        )

    def remove_par_if_meta(self, text, par, par_is_meta):
        if not par_is_meta:
            return text
        return text.replace(par, '')

    def is_par_comment(self, par):
        return par.startswith('<!--') and par.endswith('-->')

    def is_with_json(self, text):
        return text.startswith('{\n') and text.endswith('\n}')

    def fetch_pars(self, text) -> list:

        pars = re.split('\n\s{0,}\n', text)

        return list(
            filter(len, map(str.strip, pars))
        )

    def fetch_first_par(self, text) -> str:

        parts = re.split(
            '\n\s{0,}\n', text, maxsplit=1
        )

        return parts[0].strip()

    def read_source(self, filepath) -> str:
        with open(filepath, encoding='utf-8') as file:
            return file.read()

    def dumpdocpage(self, docdir, codeblocks=None):

        pagename = getattr(self, 'name') + '.html'
        pagepath = os.path.join(docdir, pagename)

        settings = self.specify_settings()
        pagehtml = self.run_pagemaker(settings, codeblocks)

        utils.dump_file(
            filepath=pagepath, content=pagehtml
        )

    def specify_settings(self):

        meta = getattr(self, 'meta')
        settings = pagemaker.PageParamsHTML()

        settings.webtitle = meta.get('webtitle', '')
        settings.doctitle = meta.get('doctitle', '')
        settings.annotation = meta.get('annotation', '')
        settings.highlights = meta.get('codeblocks', False)

        return settings

    def run_pagemaker(self, settings, codeblocks):

        sourcemd = getattr(self, 'text')

        if codeblocks is not None:
            settings.highlights = codeblocks

        return pagemaker.makedocpage(sourcemd, settings)

    def swaplinks(self):

        def swaplink(matchobj):
            return matchobj.group().replace(
                '.md', '.html'
            )

        md_link = re.compile(
            '\s\[\w{1,}\]\([\w.#]{0,}\)'
        )

        html_link = re.compile(
            '<a\s{1,}href="[\w.#]{0,}"'
        )

        self.text = re.sub(
            md_link, swaplink, self.text
        )

        self.text = re.sub(
            html_link, swaplink, self.text
        )

    def show_example_meta(self):

        meta = {
            "webtitle": 'WEBTITLE',
            "doctitle": "TITLE",
            "annotation": "ANNOTATION",
            "codeblocks": "true/false"
        }

        meta_json = self.render_json(meta)
        print(meta_json)

    def render_json(self, meta):
        return json.dumps(meta, indent=2)


class IndexFile(SourceFile):
    """The preprocessed index file.

    Attributes
    ----------
    name : str
        File name.
    text : str
        File content (edited).
    meta : dict
        Metadata for docs builder.
    toc : str
        Global TOC as an HTML list.

    """

    def __init__(self):
        super().__init__()
        self.toc = None

    def set_file(self, filepath):

        sourcemd = self.read_source(filepath)

        filename = os.path.basename(filepath).removesuffix('.md')

        self._filename = filename
        assert filename == 'index'

        sourcemd, tocashtml = self.handle_source(sourcemd)

        self.set_name(filename)
        self.set_text(sourcemd)
        self.set_meta(sourcemd)
        self.set_toc(tocashtml)

        return self

    def set_toc(self, tocashtml):
        self.toc = tocashtml

    def handle_source(self, sourcemd):

        tocastext = self.fetch_contents(sourcemd)
        tocashtml = self.contents_to_html(tocastext)

        newsource = self.update_contents(
            sourcemd, oldtoc=tocastext, newtoc=tocashtml
        )

        return newsource, tocashtml

    def update_contents(self, source, oldtoc, newtoc):
        return source.replace(oldtoc, newtoc)

    def fetch_contents(self, sourcemd):
        tocfetcher = self.fetch_contents_
        return tocfetcher(sourcemd)

    def contents_to_html(self, tocastext) -> str:
        return self.run_toc_handler(tocastext)

    def run_toc_handler(self, tocastext) -> str:
        return TocHandler().convert_toc(tocastext)

    def fetch_contents_(self, sourcemd) -> str:

        blocks = self.parse_source(sourcemd)
        index = self.find_contents_heading(blocks)
        tocasblock = self.get_list_after_heading(blocks, index)

        return tocasblock.text

    def parse_source(self, sourcemd):
        return textmd.parser.parsetext(sourcemd)

    def find_contents_heading(self, blocks) -> int | None:
        """Returns the index of contents heading, if any.
        """

        def is_contents(block):
            if not block.is_heading():
                return False
            return block.text.strip('# ') == 'Contents'

        for index, block in enumerate(blocks):
            if is_contents(block):
                return index

        return None

    def get_list_after_heading(self, blocks, heading_index):

        errmsg = ''
        index = heading_index

        if index is None:
            errmsg = "no 'Contents' heading in 'index.md'"
        if index == len(blocks) - 1:
            errmsg = "empty 'Contents' section in 'index.md'"
        if not blocks[index+1].is_list():
            errmsg = "no TOC in 'Contents' section of 'index.md'"

        if errmsg:
            raise TocNotFoundError(errmsg)

        return blocks[index+1]


class TocHandler:
    """Converts global TOC from 'index.md' to an HTML list.
    """

    def convert_toc(self, tocastext):

        tocastext = self.formattoc(tocastext)
        tocastree = self.toctext_to_tree(tocastext)
        tocashtml = self.tree_to_html_list(tocastree)

        return tocashtml

    def toctext_to_tree(self, tocastext):
        return texttrees.maketree(tocastext)

    def tree_to_html_list(self, root):
        return treeashtml.dumptree_html(root)

    def formattoc(self, tocastext):
        return self.convert_md_links(tocastext)

    def convert_md_links(self, tocastext):
        toclines = tocastext.splitlines()
        newlines = self.editlines(toclines)
        return self.assemble(newlines)

    def editlines(self, toclines) -> list:

        line_editor = self.editline

        return list(
            map(line_editor, toclines)
        )

    def editline(self, tocline):
        indent, _, link = tocline.partition('- ')
        link = self.md_link_to_html(link)
        return indent + '- ' + link

    def md_link_to_html(self, link):
        name, _, path = link.strip('[)').partition('](')
        return f'<a href="{path}">{name}</a>'.replace('.md', '.html')

    def assemble(self, lines):
        return '\n'.join(lines)


class NoIndexFileError(Exception):
    """Raised when 'index.md' is not found in the source directory.
    """


class TocNotFoundError(Exception):
    """Raised when the global TOC cannot be fetched from 'index.md'.
    """


class FileMetaDataError(Exception):
    """Raised when JSON metadata for a source file cannot be parsed.
    """
