# -*- coding: utf-8 -*-
"""Tests assembler of HTML documentation.
"""

import os
import unittest

from docspyer.docmakers.docbuilder import (
    DocsBuilder, SourceFiles, IndexFile, TocHandler
)


TOC_MD_LINKS = """
- [Alfa](alfa.md)
  - [Bravo](bravo.md)
    - [Delta]()
"""

TOC_HTML_LINKS = """
- <a href="alfa.html">Alfa</a>
  - <a href="bravo.html">Bravo</a>
    - <a href="" style="pointer-events: none;">Delta</a>
"""

INDEXMETA = {
    'webtitle': '',
    'doctitle': '',
    'annotation': '',
    'codeblocks': False
}

# Strip constants.
for key, val in list(globals().items()):
    if isinstance(val, str):
        if key.isupper():
            globals()[key] = val.strip()


def get_cwd_path():
    return os.path.dirname(__file__)


def get_file_path(filename):
    return os.path.join(
        get_cwd_path(), filename
    )


class TestTocHandler(unittest.TestCase):

    def test_format_toctext(self):
        assert TocHandler().formattoc(TOC_MD_LINKS) == TOC_HTML_LINKS


class TestIndexFile(unittest.TestCase):

    def test_extract_meta(self):

        indexmd = IndexFile().read_source(
            filepath=get_file_path('index.md')
        )

        firstpar = IndexFile().fetch_first_par(indexmd)

        assert firstpar.startswith('<!--')
        assert firstpar.endswith('-->')

        assert IndexFile().is_par_comment(firstpar) is True
        assert IndexFile().extract_meta_if_any(firstpar) == INDEXMETA

    def test_set_file(self):

        indexfile = IndexFile().set_file(
            filepath=get_file_path('index.md')
        )

        assert indexfile.meta == INDEXMETA

class TestSourceFiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        srcdir = get_cwd_path()
        sources = SourceFiles().set_sources(srcdir)

        cls.sources = sources

        cls.filenames = set(
            sources.files.keys()
        )

        cls.files = sources.files

    def test_file_names(self):
        assert self.filenames == {'alfa', 'bravo', 'index'}

    def test_contents(self):
        assert self.files['index'].toc == self.sources.contents

    def test_meta(self):
        assert self.files['bravo'].meta == {}
        assert self.files['alfa'].meta['doctitle'] == 'Alfa'
        assert self.files['index'].meta['annotation'] == ""

    def test_dumpdocpage(self):
        self.files['index'].dumpdocpage(
            docdir=get_cwd_path()
        )


class TestDocsBuilder(unittest.TestCase):

    def test_build_docs(self):

        srcdir = get_cwd_path()
        docdir = get_cwd_path()

        config = {
            'doclogo': '<div><h3>DOC-LOGO</h3></div>',
            'codeblocks': False,
            'swaplinks': True
        }

        DocsBuilder().build_docs(
            srcdir, docdir, config
        )


if __name__ == '__main__':
    unittest.main()
