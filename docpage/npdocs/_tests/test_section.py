# -*- coding: utf-8 -*-
"""Test a section in a numpy style docstring.
"""

import unittest
from docspyer.docpage.npdocs import parser

HEADING = 'Notes'

DOCS = f"""
{HEADING}
---------
"""


class TestSection(unittest.TestCase):

    block = None

    @classmethod
    def setUpClass(cls):
        cls.block = parser.parsedoc(DOCS).pop()

    def test_parse_type(self):
        assert self.block.is_section()

    def test_parse_heading(self):
        assert self.block.heading == HEADING

    def test_convert_to_md(self):
        assert self.block.render_md() == '<b>' + HEADING + '</b>'

    def test_convert_to_rst(self):
        assert self.block.render_rst() == '**' + HEADING + '**'


if __name__ == '__main__':
    unittest.main()
