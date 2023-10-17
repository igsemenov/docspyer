# -*- coding: utf-8 -*-
"""Test the convert of numpy style docstrings.
"""

import os
import inspect
import unittest
from docspyer.docpage.npdocs import convert


def myfunc():
    """MYFUNCTION

    Parameters
    ----------
    VAR1 : TYPE1
        ONELINEDOC
    VAR2 : TYPE2
        MULTILINE
            DESCRIPTION

    Returns
    -------
    TYPE
        DESCRIPTION

    Notes
    -----
    SOMETEXT

    """


class TestConverter(unittest.TestCase):

    def test_docasmd(self):

        dirpath = os.path.dirname(__file__)

        filepath = os.path.join(
            dirpath, '_npdocstr.md'
        )

        docstr = inspect.getdoc(myfunc)
        docstr_md = convert.docasmd(docstr)

        with open(filepath, encoding='utf-8', mode='w') as file:
            file.write(docstr_md)

    def test_docasrst(self):

        dirpath = os.path.dirname(__file__)

        filepath = os.path.join(
            dirpath, '_npdocstr.rst'
        )

        docstr = inspect.getdoc(myfunc)
        docstr_md = convert.docasrst(docstr)

        with open(filepath, encoding='utf-8', mode='w') as file:
            file.write(docstr_md)


if __name__ == '__main__':
    unittest.main()
