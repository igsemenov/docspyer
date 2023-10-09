# -*- coding: utf-8 -*-
"""Test variable lists in numpy style docstrings.
"""

import unittest
from docspyer.docpage.npdocs import parser
from docspyer.docpage.npdocs import blocks


PARAMS = """
Parameters
----------
VAR1 : TYPE1
    ONLINEDOC
VAR2 : TYPE2
    MULTILINE
      DOC
"""

RETURNS = """
Returns
-------
TYPE
    ONELINEDOC
"""


class TestParams(unittest.TestCase):

    block = None

    var1 = None
    var2 = None

    @classmethod
    def setUpClass(cls):

        cls.block = parser.parsedoc(PARAMS).pop()

        cls.var1 = cls.block.variables[0]
        cls.var2 = cls.block.variables[1]

    def test_heading(self):
        assert self.block.heading == 'Parameters'

    def test_varnames(self):
        assert self.var1.varname == 'VAR1'
        assert self.var2.varname == 'VAR2'

    def test_vartypes(self):
        assert self.var1.vartype == 'TYPE1'
        assert self.var2.vartype == 'TYPE2'

    def test_onelinedoc(self):
        assert self.var1.vardoc == 'ONLINEDOC'

    def test_multilinedoc(self):
        assert self.var2.vardoc == 'MULTILINE\n  DOC'


class TestReturns(unittest.TestCase):

    block = None
    var = None

    @classmethod
    def setUpClass(cls):
        cls.block = parser.parsedoc(RETURNS).pop()
        cls.var = cls.block.variables.pop()

    def test_heading(self):
        assert self.block.heading == 'Returns'

    def test_varname(self):
        assert self.var.varname == 'TYPE'

    def test_vartype(self):
        assert self.var.vartype == ''

    def test_vardoc(self):
        assert self.var.vardoc == 'ONELINEDOC'


class TestRendering(unittest.TestCase):

    VARLIST = blocks.Varlist(
        heading='Parameters', varrecords=[]
    )

    def test_render_md(self):
        assert self.VARLIST.render_md() == '<b>Parameters</b>'

    def test_render_rst(self):
        assert self.VARLIST.render_rst() == '**Parameters**'


if __name__ == '__main__':
    unittest.main()
