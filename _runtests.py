# -*- coding: utf-8 -*-
"""Script for running the tests.
"""

import unittest

suite = unittest.TestSuite()

dirnames = [
    'utils',
    'inspect',
    'docpage',
    'docpage/textmd',
    'docpage/npdocs',
    'docmakers'
]


for dirname in dirnames:

    dirsuite = unittest.TestLoader().discover(
        start_dir=dirname + '/_tests', pattern='test_*.py'
    )

    suite.addTests(dirsuite)

unittest.TextTestRunner(verbosity=0).run(suite)
