# -*- coding: utf-8 -*-
"""Dumps functions and classes to RST entries.
"""

import textwrap
from . import pydump
from ..docpage import npdocs

__all__ = [
    'modtorst'
]


def apiobj(obj):
    obj.__module__ = 'docspy.inspect'
    return obj


@apiobj
def modtorst(pymod) -> str:
    """Dumps functions and classes from a module in RST format.

    Parameters
    ----------
    pymod : module
        A python module to be documented.

    Returns
    -------
    str
        The resulting RST document.

    """

    dumper = set_object_dumper()

    entries = pydump.docmembers(
        pymod, dumper
    )

    name = pymod.__name__
    heading = name + '\n' + '='*len(name)
    definition = '.. py:module:: ' + name

    return '\n\n'.join(
        [heading, definition, entries]
    )


def set_object_dumper():
    return dumpobj


def dumpobj(obj) -> str:

    func_dumper = functorst
    class_dumper = classtorst

    if obj.__class__.__name__ == 'function':
        return func_dumper(
            obj, doceditor=npdocs.docasrst
        )

    if obj.__class__.__name__ == 'type':
        return class_dumper(
            obj, doceditor=npdocs.docasrst
        )

    return ''


def functorst(pyfunc, doceditor=None) -> str:
    """Dumps a python function to an RST entry.

    Parameters
    ----------
    pyfunc : function
        Function to be documented.
    doceditor : function
        Can by applied to edit the docstring.

    Returns
    -------
    str
        The resulting RST entry.

    """

    if type(pyfunc).__name__ != 'function':
        raise ValueError('argument is not a function')

    funcdumper = FuncDumperRST()
    funcdumper.set_doceditor_if_any(doceditor)

    return funcdumper.dumpobj(pyfunc)


def classtorst(pyclass, doceditor=None) -> str:
    """Dumps a python class to an RST entry.

    Parameters
    ----------
    pyclass : type
        Class to be documented.
    doceditor : function
        May by applied to edit the docstring.

    Returns
    -------
    str
        The resulting RST entry.

    """

    if type(pyclass).__name__ != 'type':
        raise ValueError('argument is not a class')

    methodsdumper = set_methodsdumper(doceditor)
    classdumper = set_classdumper(doceditor, methodsdumper)

    return classdumper.dumpobj(pyclass)


def set_methodsdumper(doceditor):
    methodsdumper = FuncDumperRST()
    methodsdumper.set_doceditor_if_any(doceditor)
    return methodsdumper


def set_classdumper(doceditor, methodsdumper):

    classdumper = ClassDumperRST()

    classdumper.set_doceditor_if_any(doceditor)
    classdumper.set_funcsdumper(methodsdumper)

    return classdumper


class DumperRST:

    PREFIX = 3*chr(32)

    def format_header(self, name, signature):
        _, _, given_name = name.rpartition('.')
        return self.make_definition(given_name, signature)

    def apply_doceditor_if_any(self, docs):
        if hasattr(self, 'doceditor'):
            newdocs = getattr(self, 'doceditor')(docs)
            return self.indent_text(newdocs)
        return None

    def dump_docs_as_text_otherwise(self, docs):

        if not docs:
            return ''

        text = self.make_text_block(docs)
        return self.indent_text(text)

    def make_text_block(self, docs):
        return '.. code-block::\n\n' + self.indent_text(docs)

    def make_definition(self, name, signature):
        return name + signature

    def indent_text(self, text):
        return textwrap.indent(
            text, prefix=self.PREFIX
        )


class FuncDumperRST(DumperRST, pydump.FuncDumper):

    def make_definition(self, name, signature):
        return self.as_py_function(name, signature)

    def as_py_function(self, name, signature):
        return '.. py:function:: ' + name + signature


class ClassDumperRST(DumperRST, pydump.ClassDumper):

    def make_definition(self, name, signature):
        return self.as_py_class(name, signature)

    def as_py_class(self, name, signature):
        return '.. py:class:: ' + name + signature

    def format_content(self, docs, funcs):
        return self.join_docs_and_methods(docs, funcs)

    def join_docs_and_methods(self, docs, funcs):
        return '\n\n'.join(
            filter(len, [docs, funcs])
        )

    def func_entry_to_method(self, entry):
        entry = self.change_label(entry)
        entry = self.remove_self(entry)
        return self.indent_text(entry)

    def change_label(self, entry):
        return entry.replace(
            'py:function::', 'py:method::'
        )

    def remove_self(self, entry):

        if not '(self' in entry:
            return entry

        left, _, right = entry.partition('(self')
        return left + '(' + right.lstrip(', ')
