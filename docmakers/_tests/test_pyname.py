# -*- coding: utf-8 -*-
"""Tests utility functions and classes.
"""

import unittest
from docspyer.docmakers import utils

PyName = utils.PyName


class TestPyName(unittest.TestCase):

    SAMPLES = [
        'mod.', 'mod.func', 'mod.CONST',
        'mod.Class', 'mod.Class.func', 'mod.Class.CONST',
        'pkg.mod.Class', 'pkg.mod.Class.func', 'pkg.mod.Class.CONST'
    ]

    def test_attr_mod(self):

        pyname = PyName()

        for val in self.SAMPLES:

            ref = self._get_ref_mod(val)

            self.assertEqual(
                pyname.fromstr(val).getmodule(), ref, val
            )

    def _get_ref_mod(self, val):
        if val.startswith('mod.'):
            return 'mod'
        if val.startswith('pkg.mod.'):
            return 'pkg.mod'

    def test_attr_cls(self):

        pyname = PyName()

        for val in self.SAMPLES:

            ref = 'Class' if 'Class' in val else ''

            self.assertEqual(
                pyname.fromstr(val).getclass(), ref, val
            )

    def test_attr_name(self):

        pyname = PyName()

        for val in self.SAMPLES:

            ref = self._get_ref_name(val)

            self.assertEqual(
                pyname.fromstr(val).getname(), ref, val
            )

    def _get_ref_name(self, val):
            if '.func' in val:
                return 'func'
            if '.CONST' in val:
                return 'CONST'
            return ''


if __name__ == '__main__':
    unittest.main()
