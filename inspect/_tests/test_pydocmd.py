# -*- coding: utf-8 -*-
"""Test dumpers of python objects in MD format.
"""

import os
import unittest
from docspyer.inspect import pydocmd


def myfunc(arg1, arg2) -> int:
    """FUNCDOCS
    """
    return arg1 + arg2


class MyBase:

    def basemethod(self) -> None:
        """BASEMETHOD
        """


class MyClass(MyBase):
    """CLASSDOCS
    """

    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def basemethod(self) -> None:
        pass

    def mymethod(self):
        """METHODDOCS
        """


myfunc.__module__ = 'mymodule'
MyClass.__module__ = 'mymodule'


def editdocs(docs):
    return docs


class TestDumpers(unittest.TestCase):

    def test_functomd_basic(self):

        dumper = pydocmd.get_objdumper()
        dumper.set_dumper()

        out = dumper.dumpobj(myfunc)

        assert ' → ' in out
        assert '```docstring\n' in out

    def test_functomd_full(self):

        dumper = pydocmd.get_objdumper()

        dumper.set_dumper(
            hostname='mymodule', doceditor=editdocs, level=2
        )

        out = dumper.dumpobj(myfunc)

        assert 'myfunc()' in out

        _dumpfile(out, '_myfunc.md')


class TestClassDumper(unittest.TestCase):

    def test_classtomd_basic(self):

        dumper = pydocmd.get_objdumper()
        dumper.set_dumper()

        out = dumper.dumpobj(MyClass)

        assert out.count('```docstring\n') == 3

    def test_classtomd_full(self):

        dumper = pydocmd.get_objdumper()

        dumper.set_dumper(
            hostname='mymodule', doceditor=editdocs, level=2
        )

        out = dumper.dumpobj(MyClass)

        _dumpfile(out, '_myclass.md')


def _dumpfile(content, filename):

    dirpath = os.path.dirname(__file__)

    filepath = os.path.join(
        dirpath, filename
    )

    with open(filepath, encoding='utf-8', mode='w') as file:
        file.write(content)


if __name__ == '__main__':
    unittest.main()
