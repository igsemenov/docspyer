# -*- coding: utf-8 -*-
"""Test the parser of numpy style docstrings.
"""

import unittest
from docspyer.docpage.npdocs import parser


class TestParser(unittest.TestCase):

    def test_fetchpars(self):

        fetchpars = parser.fetchpars

        assert fetchpars('') == []
        assert fetchpars('A') == ['A']
        assert fetchpars('\nA\n') == ['A']
        assert fetchpars('A\n\nB') == ['A', 'B']

    def test_find_type(self):

        find_partype = parser.ParReader().find_partype

        assert find_partype('') == 'textdata'
        assert find_partype('A') == 'textdata'

        assert find_partype('Parameters\n---') == 'varlist'
        assert find_partype('Parameters\n---\n') == 'varlist'

        assert find_partype('Notes\n---') == 'section'
        assert find_partype('Notes\n---\n') == 'section'


class TestFactories(unittest.TestCase):

    def test_factory_section(self):

        make_block = parser.SectionFactory().make_block

        assert make_block('Notes\n---').is_section()
        assert make_block('Notes\n---').heading == 'Notes'
        assert make_block('Notes\n---').content == ''
        assert make_block('Notes\n---\nText').content == 'Text'

    def test_factory_varlist(self):

        make_block = parser.VarlistFactory().make_block

        assert make_block('Parameters\n---').is_varlist()
        assert make_block('Parameters\n---').heading == 'Parameters'
        assert make_block('Parameters\n---').variables == []
        assert make_block('Parameters\n---\n').variables == []

    def test_factory_textata(self):

        make_block = parser.TextdataFactory().make_block

        assert make_block('').is_textdata()


class TestVarReader(unittest.TestCase):

    def test_fetch_varname(self):

        fetch_varname = parser.VarReader().fetch_varname

        assert fetch_varname('var') == 'var'
        assert fetch_varname('var  ') == 'var'
        assert fetch_varname('var : type') == 'var'

    def test_fetch_vartype(self):

        fetch_vartype = parser.VarReader().fetch_vartype

        assert fetch_vartype('var') == ''
        assert fetch_vartype('var  ') == ''
        assert fetch_vartype('var : type') == 'type'

    def test_make_record(self):
        make_record = parser.VarReader().make_record
        assert make_record(vardef='', vardoc='').is_varrecord()


if __name__ == '__main__':
    unittest.main()
