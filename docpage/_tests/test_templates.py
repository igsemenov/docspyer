# -*- coding: utf-8 -*-
"""Test template files.
"""

import unittest
from docspyer.docpage import templates

PAGEHTML = templates.DocPageHTML()
PAGEJS = templates.DocPageJS()

PARAMS_HTML = templates.PageParamsHTML()
PARAMS_JS = templates.PageParamsJS()

PARAMS_HTML.webtitle = 'A+'
PARAMS_HTML.doctitle = 'B*'
PARAMS_HTML.annotation = 'C~'
PARAMS_HTML.localtoc = '?alfa->'
PARAMS_HTML.pagetext = '?bravo->'

PARAMS_JS.pagelogo = 'X?'
PARAMS_JS.homepage = 'X+'
PARAMS_JS.contents = 'X~'


class TestDocPageHTML(unittest.TestCase):

    def test_no_params(self):
        assert PAGEHTML.getpage() == PAGEHTML.getsource()

    def test_webtitle(self):
        assert '<title>A+</title>' in PAGEHTML.getpage(PARAMS_HTML)

    def test_doctitle(self):
        assert '>B*</h1>' in PAGEHTML.getpage(PARAMS_HTML)

    def test_annotation(self):
        assert '>C~</h2>' in PAGEHTML.getpage(PARAMS_HTML)

    def test_localtoc(self):
        assert ' ?alfa->' in PAGEHTML.getpage(PARAMS_HTML)

    def test_pagetext(self):
        assert '?bravo->' in PAGEHTML.getpage(PARAMS_HTML)


class TestDocPageJS(unittest.TestCase):

    def test_getpage_no_params(self):
        assert PAGEJS.getpage() == PAGEJS.getsource()

    def test_pagelogo(self):
        assert '.pagelogo = `X?`;' in PAGEJS.getpage(PARAMS_JS)

    def test_homepage(self):
        assert '.homepage = `X+`;' in PAGEJS.getpage(PARAMS_JS)

    def test_contents(self):
        assert '.contents = `X~`;' in PAGEJS.getpage(PARAMS_JS)


if __name__ == '__main__':
    unittest.main()
