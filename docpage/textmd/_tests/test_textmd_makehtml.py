# -*- coding: utf-8 -*-
import unittest
from docspyer.docpage.textmd import blocks
from docspyer.docpage.textmd import makehtml

Heading = blocks.MDHeading

TOCMaker = makehtml.TOCMaker
DocMaker = makehtml.DocMaker


TEXTMD = """
# Alfa

## Bravo
"""

TEXTHTML = """
<div class="toc-anchor"></div><h1>Alfa</h1>

<div class="toc-anchor"></div><h2>Bravo</h2>
"""

HEADINGS = [
    Heading('# Alfa'), Heading('## Bravo')
]

TOC_AS_LIST = """
- <a href="#alfa">Alfa</a>
  - <a href="#bravo">Bravo</a>
"""

TOC_IN_HTML = """
<p>
<ul>
    <li><a href="#alfa">Alfa</a>
        <ul>
            <li><a href="#bravo">Bravo</a></li>
        </ul>
    </li>
</ul>
</p>
"""

# Strip constants.
for key, val in list(globals().items()):
    if isinstance(val, str):
        if key.isupper():
            globals()[key] = val.strip()


class TestConverter(unittest.TestCase):

    def test_convert(self):

        dochtml = DocMaker().make_dochtml(TEXTMD)

        assert dochtml.text == TEXTHTML.strip()
        assert dochtml.toc == TOC_IN_HTML.strip()


class TestTOCMaker(unittest.TestCase):

    def test_make_toc_as_list(self):
        assert TOCMaker().make_toc_as_list(HEADINGS) == TOC_AS_LIST

    def test_toc_in_html(self):
        assert TOCMaker().maketoc(HEADINGS) == TOC_IN_HTML


if __name__ == '__main__':
    unittest.main()
