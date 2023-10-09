# -*- coding: utf-8 -*-
"""Test inclusion of subtrees into trees.
"""

import os
import unittest
from docspy.inspect import pydocmd
from docspy.inspect import pydocrst

functomd = pydocmd.functomd
classtomd = pydocmd.classtomd

functorst = pydocrst.functorst
classtorst = pydocrst.classtorst


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


def doceditor(docs):
    return docs


def dumpfile(content, filename):

    dirpath = os.path.dirname(__file__)

    filepath = os.path.join(
        dirpath, filename
    )

    with open(filepath, encoding='utf-8', mode='w') as file:
        file.write(content)


def run_dumper(objtype, mode):

    dumper = globals()[objtype + 'to' + mode]

    if objtype == 'func':
        obj = myfunc
    if objtype == 'class':
        obj = MyClass

    obj_primary = dumper(obj)

    obj_edited = dumper(
        obj, doceditor=doceditor
    )

    title_primary = '\n\n'.join(
        ['**CASE-NO-DOCEDITOR**', '-----']
    )

    title_edited = '\n\n'.join(
        ['**CASE-WITH-DOCEDITOR**', '-----']
    )

    obj_primary = title_primary + '\n\n' + obj_primary
    obj_edited = title_edited + '\n\n' + obj_edited

    content = '\n\n'.join(
        [obj_primary, obj_edited]
    )

    dumpfile(
        content, f'_{objtype}.{mode}'
    )


class TestFuncDumper(unittest.TestCase):

    def test_functomd(self):
        run_dumper('func', 'md')

    def test_functorst(self):
        run_dumper('func', 'rst')

    def test_functomd_level(self):
        funcmd = functomd(myfunc, level=1)
        assert funcmd.startswith('# myfunc()\n\n')


class TestClassDumper(unittest.TestCase):

    def test_classtomd(self):
        run_dumper('class', 'md')

    def test_classtorst(self):
        run_dumper('class', 'rst')

    def test_classtomd_level(self):
        classmd = classtomd(MyClass, level=1)
        assert classmd.startswith('# MyClass\n\n')


if __name__ == '__main__':
    unittest.main()
