# -*- coding: utf-8 -*-
"""Test the editor of inline patterns.
"""

import unittest
from docspyer.docpage.textmd import emphase

editor = emphase.edit_inline_md

TEXT_MD = """
`CODE`,
"MARK",
**BOLD**,
*ITALIC*,
***STRONG***
"""

TEXT_HTML = """
<code>CODE</code>,
<i>&quot;MARK&quot;</i>,
<b>BOLD</b>,
<em>ITALIC</em>,
<b><em>STRONG</em></b>
"""

LINK_MD = ' [Alfa](alfa.md) '
LINK_HTML = ' <a href="alfa.md">Alfa</a> '


class TestPatterns(unittest.TestCase):

    def test_text_with_patterns(self):
        assert editor(TEXT_MD) == TEXT_HTML

    def test_backticks(self):
        assert editor('`TEXT`') == '<code>TEXT</code>'

    def test_quotmarks(self):
        assert editor('"TEXT"') == '<i>&quot;TEXT&quot;</i>'

    def test_asterisks_bold(self):
        assert editor('**TEXT**') == '<b>TEXT</b>'

    def test_asterisks_italics(self):
        assert editor('*TEXT*') == '<em>TEXT</em>'

    def test_asterisks_bold_italix(self):
        assert editor('***TEXT***') == '<b><em>TEXT</em></b>'

    def test_links(self):
        assert editor(LINK_MD) == LINK_HTML

    def test_links_with_punctuation(self):

        for mark in ',.:':

            link_md = LINK_MD.rstrip() + mark
            link_html = LINK_HTML.rstrip() + mark

            assert editor(link_md) == link_html


if __name__ == '__main__':
    unittest.main()
