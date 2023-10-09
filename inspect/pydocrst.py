# -*- coding: utf-8 -*-
"""Dumps module members to RST entries.
"""

import textwrap
from . import pydump
from ..docpage import npdocs

__all__ = [
    'modtorst'
]


def apiobj(obj):
    obj.__module__ = 'docspyer.inspect'
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

    name = pymod.__name__
    docs = pymod.__doc__ or ''

    docs = npdocs.docasrst(docs)

    dumper = get_object_dumper()

    dumper.set_dumper(
        hostname=name, doceditor=npdocs.docasrst, level=2
    )

    entries = pydump.docmod_with_dumper(pymod, dumper)

    heading = name + '\n' + '='*len(name)
    definition = '.. py:module:: ' + name

    parts = [
        heading, definition, entries
    ]

    return '\n\n'.join(
        filter(len, parts)
    )


def get_object_dumper():

    dumpertypes = {
        'func': FuncDumperRST,
        'class': ClassDumperRST
    }

    return pydump.ObjectDumper(dumpertypes)


class DumperRST:

    PREFIX = 3*chr(32)

    def formatdoc(self, docs):
        return self.make_text_block(docs)

    def make_text_block(self, docs):
        return '.. code-block::\n\n' + self.indent_text(docs)

    def indent_text(self, text):
        return textwrap.indent(
            text, prefix=self.PREFIX
        )

    def format_content(self, content):
        return content


class FuncDumperRST(DumperRST, pydump.FuncDumper):
    """Dumps functions in RST format.
    """

    def build_header(self, name, signature):
        return self.as_py_function(name, signature)

    def as_py_function(self, name, signature):
        return '.. py:function:: ' + name + signature


class ClassDumperRST(DumperRST, pydump.ClassDumper):
    """Dumps classes in RST format.
    """

    def build_header(self, name, signature):
        return self.as_py_class(name, signature)

    def as_py_class(self, name, signature):
        return '.. py:class:: ' + name + signature

    def format_method_entry(self, entry):
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
