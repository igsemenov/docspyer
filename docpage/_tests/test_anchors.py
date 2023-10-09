# -*- coding: utf-8 -*-
"""Test anchors in template files.
"""
import unittest
from docspyer.docpage import anchors
from docspyer.docpage import templates


class AnchorTester:

    ANCHOR = None
    SOURCE = None

    def anchor_line(self):
        return self.ANCHOR.find_anchor_line(self.SOURCE)

    def source_anchor_replaced(self):
        return self.ANCHOR.replace_anchor(self.SOURCE)

    def source_anchor_removed(self):
        return self.ANCHOR.remove_anchor(self.SOURCE)


class TestAnchor(AnchorTester):

    def test_find_anchor_line(self):
        assert self.anchor_line() is not None


class TestHeader(TestAnchor):

    SOURCE = templates.DocPageHTML().getsource()


class TestPageContent(TestAnchor):

    SOURCE = templates.DocPageHTML().getsource()


class TestPageSettings(TestAnchor):

    SOURCE = templates.DocPageJS().getsource()

    def test_replace_anchor(self):
        assert self.source_anchor_replaced() == self.SOURCE


class TestHighlight(TestAnchor):

    SOURCE = templates.DocPageHTML().getsource()

    def test_replace_anchor(self):
        assert self.ANCHOR.REPL in self.source_anchor_replaced()

    def test_remove_anchor(self):
        assert self.ANCHOR.TEXT not in self.source_anchor_removed()

    def test_get_replacement(self):
        assert self.ANCHOR.get_replacement() == self.ANCHOR.REPL


class TestWebtitle(TestHeader, unittest.TestCase):

    ANCHOR = anchors.Webtitle()


class TestDoctitle(TestHeader, unittest.TestCase):

    ANCHOR = anchors.Doctitle()


class TestAnnotation(TestHeader, unittest.TestCase):

    ANCHOR = anchors.Annotation()


class TestLocalTOC(TestPageContent, unittest.TestCase):

    ANCHOR = anchors.LocalTOC()


class TestPageText(TestPageContent, unittest.TestCase):

    ANCHOR = anchors.PageText()


class TestPageLogo(TestPageSettings, unittest.TestCase):

    ANCHOR = anchors.PageLogo()


class TestGlobalTOC(TestPageSettings, unittest.TestCase):

    ANCHOR = anchors.GlobalTOC()


class TestHomePage(TestPageSettings, unittest.TestCase):

    ANCHOR = anchors.HomePage()


class TestHighlightJS(TestHighlight, unittest.TestCase):

    ANCHOR = anchors.HighlightJS()


class TestHighlightCSS(TestHighlight, unittest.TestCase):

    ANCHOR = anchors.HighlightCSS()


class TestHighlightFunc(TestHighlight, unittest.TestCase):

    ANCHOR = anchors.HighlightFunc()


if __name__ == '__main__':
    unittest.main()
