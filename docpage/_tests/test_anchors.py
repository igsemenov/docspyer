# -*- coding: utf-8 -*-
"""Test anchors in template files.
"""

import unittest
from docspyer.docpage import anchors
from docspyer.docpage import templates


class TestAnchor:

    anchor = None
    source = None

    def test_find_anchor_line(self):

        anchor = self.anchor
        source = self.source

        assert anchor.find_anchor_line(source) is not None, 'Anchor'


class TestHeader(TestAnchor):

    source = templates.DocPageHTML().getsource()


class TestPageContent(TestAnchor):

    source = templates.DocPageHTML().getsource()


class TestPageSettings(TestAnchor):

    source = templates.DocPageJS().getsource()

    def test_replace_anchor(self):

        anchor = self.anchor
        source = self.source

        assert anchor.replace_anchor(source) == source, 'PageSettings'


class TestHighlight(TestAnchor):

    source = templates.DocPageHTML().getsource()

    def test_set_replacement(self):

        anchor = self.anchor

        assert anchor.set_replacement() == anchor.REPL, 'Highlight'

    def test_replace_anchor(self):

        anchor = self.anchor
        source = self.source

        newsource = anchor.replace_anchor(source)

        assert anchor.REPL not in source, 'Highlight'
        assert anchor.REPL in newsource, 'Highlight'

    def test_remove_anchor(self):

        anchor = self.anchor
        source = self.source

        newsource = anchor.remove_anchor(source)

        assert anchor.TEXT in source, 'Highlight'
        assert anchor.TEXT not in newsource, 'Highlight'


class TestWebtitle(TestHeader, unittest.TestCase):
    anchor = anchors.Webtitle()


class TestDoctitle(TestHeader, unittest.TestCase):
    anchor = anchors.Doctitle()


class TestAnnotation(TestHeader, unittest.TestCase):
    anchor = anchors.Annotation()


class TestLocalTOC(TestPageContent, unittest.TestCase):
    anchor = anchors.LocalTOC()


class TestPageText(TestPageContent, unittest.TestCase):
    anchor = anchors.PageText()


class TestPageLogo(TestPageSettings, unittest.TestCase):
    anchor = anchors.PageLogo()


class TestGlobalTOC(TestPageSettings, unittest.TestCase):
    anchor = anchors.GlobalTOC()


class TestHomePage(TestPageSettings, unittest.TestCase):
    anchor = anchors.HomePage()


class TestHighlightJS(TestHighlight, unittest.TestCase):
    anchor = anchors.HighlightJS()


class TestHighlightCSS(TestHighlight, unittest.TestCase):
    anchor = anchors.HighlightCSS()


class TestHighlightFunc(TestHighlight, unittest.TestCase):
    anchor = anchors.HighlightFunc()


if __name__ == '__main__':
    unittest.main()
