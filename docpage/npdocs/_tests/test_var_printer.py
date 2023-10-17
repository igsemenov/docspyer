# -*- coding: utf-8 -*-
"""Test variable records from variable lists.
"""

import unittest
from docspyer.docpage.npdocs import printers

printer = printers.VarPrinter()

VARNAME = '<code>VAR</code>'
VARTYPE = '<em>TYPE</em>'

VARDEF_NO_TYPE = '<em>VAR</em>'
VARDEF_WITH_TYPE = f'{VARNAME} : {VARTYPE}'

VARDOC = '<dl><dd>\n  DOC\n</dd></dl>'


class TestPrinter(unittest.TestCase):

    def test_render_varname(self):
        assert printer.render_vartype('') == ''
        assert printer.render_varname('VAR') == VARNAME

    def test_render_vartype(self):
        assert printer.render_vartype('') == ''
        assert printer.render_vartype('TYPE') == VARTYPE

    def test_render_vardoc(self):
        assert printer.render_vardoc('DOC') == VARDOC

    def test_render_vardef_no_type(self):
        assert printer.make_vardef('VAR', '') == VARDEF_NO_TYPE

    def test_render_vardef_with_type(self):
        assert printer.make_vardef('VAR', 'TYPE') == VARDEF_WITH_TYPE


if __name__ == '__main__':
    unittest.main()
