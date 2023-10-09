# -*- coding: utf-8 -*-
"""Test dumpers of python objects in MD format.
"""

import os
import unittest
from docspyer.inspect import pydocrst


def myfunc(arg1, arg2) -> int:
    """FUNCDOCS
    """
    return arg1 + arg2


class MyClass:
    """CLASSDOCS
    """

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def mymethod(self):
        """METHODDOCS
        """


myfunc.__module__ = 'mymodule'
MyClass.__module__ = 'mymodule'


def editdocs(docs):
    return docs


class TestDumpers(unittest.TestCase):

    def test_functomd_basic(self):

        dumper = pydocrst.get_object_dumper()
        dumper.set_dumper()

        out = dumper.dumpobj(myfunc)

        assert '.. code-block::\n' in out
        assert '\n   FUNCDOCS' in out

    def test_functomd_full(self):

        dumper = pydocrst.get_object_dumper()

        dumper.set_dumper(
            hostname='mymodule', doceditor=editdocs, level=2
        )

        out = dumper.dumpobj(myfunc)

        _dumpfile(out, '_myfunc.rst')


class TestClassDumper(unittest.TestCase):

    def test_classtomd_basic(self):

        dumper = pydocrst.get_object_dumper()
        dumper.set_dumper()

        out = dumper.dumpobj(MyClass)

        assert out.count('.. code-block::') == 2

    def test_classtomd_full(self):

        dumper = pydocrst.get_object_dumper()

        dumper.set_dumper(
            hostname='mymodule', doceditor=editdocs, level=2
        )

        out = dumper.dumpobj(MyClass)

        _dumpfile(out, '_myclass.rst')


def _dumpfile(content, filename):

    dirpath = os.path.dirname(__file__)

    filepath = os.path.join(
        dirpath, filename
    )

    with open(filepath, encoding='utf-8', mode='w') as file:
        file.write(content)


if __name__ == '__main__':
    unittest.main()
