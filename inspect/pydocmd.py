# -*- coding: utf-8 -*-
"""Dumps functions and classes to MD entries.
"""

import json
from . import pydump
from ..docpage import npdocs

__all__ = [
    'modtomd'
]


def apiobj(obj):
    obj.__module__ = 'docspy.inspect'
    return obj


@apiobj
def modtomd(pymod, meta=None) -> str:
    """Dumps functions and classes from a module in MD format.

    Parameters
    ----------
    pymod : module
        A python module to be documented.
    meta : dict
        Metadata added as a header to the output document.
        If the argument is not empty or None, it is formatted 
        as a JSON string enclosed by an HTML comment.
        Otherwise, the argument is ignored.

    Returns
    -------
    str
        The resulting MD document.

    """

    dumper = set_object_dumper()

    docs = pymod.__doc__ or ''
    docs = npdocs.docasmd(docs)

    meta = format_meta(meta)
    heading = '# ' + pymod.__name__
    entries = pydump.docmembers(pymod, dumper)

    parts = [
        meta, heading, docs, entries
    ]

    return '\n\n'.join(
        filter(len, parts)
    )


def set_object_dumper():
    return dumpobj


def format_meta(meta):

    if not meta:
        return ''

    meta = json.dumps(meta, indent=2)
    return f'<!--\n{meta}\n-->'


def dumpobj(obj) -> str:

    func_dumper = functomd
    class_dumper = classtomd

    if obj.__class__.__name__ == 'function':
        return func_dumper(
            obj, level=2, doceditor=npdocs.docasmd
        )

    if obj.__class__.__name__ == 'type':
        return class_dumper(
            obj, level=2, doceditor=npdocs.docasmd
        )

    return ''


def functomd(pyfunc, level=None, doceditor=None) -> str:
    """Dumps a python function to an MD entry.

    Parameters
    ----------
    pyfunc : function
        Function to be documented.
    level : int
        Level of the entry heading.
    doceditor : function
        Can by applied to edit the docstring.

    Returns
    -------
    str
        The resulting MD entry.

    """

    if type(pyfunc).__name__ != 'function':
        raise ValueError('argument is not a function')

    funcdumper = FuncDumperMD()

    funcdumper.set_level_if_any(level)
    funcdumper.set_doceditor_if_any(doceditor)

    return funcdumper.dumpobj(pyfunc)


def classtomd(pyclass, level=None, doceditor=None) -> str:
    """Dumps a python class to an MD entry.

    Parameters
    ----------
    pyclass : type
        Class to be documented.
    level : int
        Level of the entry heading.
    doceditor : function
        May by applied to edit the docstring.

    Returns
    -------
    str
        The resulting MD entry.

    """

    if type(pyclass).__name__ != 'type':
        raise ValueError('argument is not a class')

    methodsdumper = set_methodsdumper(level, doceditor)
    classdumper = set_classdumper(level, doceditor, methodsdumper)

    return classdumper.dumpobj(pyclass)


def set_methodsdumper(level, doceditor):

    if level:
        level += 1

    methodsdumper = FuncDumperMD()
    methodsdumper.set_level_if_any(level)
    methodsdumper.set_doceditor_if_any(doceditor)

    return methodsdumper


def set_classdumper(level, doceditor, methodsdumper):

    classdumper = ClassDumperMD()

    classdumper.set_level_if_any(level)
    classdumper.set_doceditor_if_any(doceditor)
    classdumper.set_funcsdumper(methodsdumper)

    return classdumper


class DumperMD:

    def set_level_if_any(self, level):
        if level is None:
            return
        setattr(self, 'level', level)

    def format_header(self, name, signature):
        heading = self.make_heading_if_level(name)
        definition = self.make_definition(name, signature)
        return self.assemble(heading, definition)

    def make_definition(self, name, signature):
        return name + signature

    def make_heading_if_level(self, name):

        level = getattr(self, 'level', None)

        if level is None:
            return ''

        _, _, given_name = name.rpartition('.')

        title = self.make_title(given_name)
        return '#'*level + chr(32) + title

    def make_title(self, objname):
        if not objname.islower():
            return objname
        return objname + '()'

    def format_name(self, name) -> str:
        base_name, _, given_name = name.rpartition('.')
        given_name = '<b>' + given_name + '</b>'
        return base_name + '.' + given_name

    def formatsignature(self, signature) -> str:
        signature = self.format_return_annot(signature)
        signature = self.format_params(signature)
        return signature

    def format_return_annot(self, signature):

        if '->' not in signature:
            return signature

        body, _, annot = signature.rpartition(' -> ')
        return body + ' → ' + f'<em>{annot}</em>'

    def format_params(self, signature):

        for key in ['None', 'True', 'False']:
            signature = signature.replace(
                f'={key}', f'=<span>{key}</span>'
            )

        signature = signature.replace('(self', '(<em>self</em>')
        signature = signature.replace('(cls', '(<em>cls</em>')

        return signature

    def dump_docs_as_text_otherwise(self, docs):
        return f'```docstring\n{docs}\n```'

    def dump_pre_py_sign(self, content):
        return f'<pre class="py-sign">{content}</pre>'

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )


class FuncDumperMD(DumperMD, pydump.FuncDumper):

    def make_definition(self, name, signature):
        text = self.format_name(name) + signature
        return self.dump_pre_py_sign(text)


class ClassDumperMD(DumperMD, pydump.ClassDumper):

    def make_definition(self, name, signature):
        newname = self.format_name(name)
        text = newname + signature
        text = self.add_class_word(text)
        return self.dump_pre_py_sign(text)

    def add_class_word(self, text):
        return '<b><em>class</em></b> ' + text

    def format_content(self, docs, funcs):
        return self.join_docs_and_methods(docs, funcs)

    def join_docs_and_methods(self, docs, funcs):

        return '\n\n'.join(
            filter(len, [docs, funcs])
        )

    def func_entry_to_method(self, entry):
        entry = self.change_prolog(entry)
        return entry

    def change_prolog(self, entry):

        prolog, _, _ = entry.partition('.<b>')
        prolog_no_class, _, classname = prolog.rpartition('.')
        _, _, modname = prolog_no_class.rpartition('>')

        newprolog = prolog.replace(
            modname + '.' + classname, classname
        )

        entry = entry.replace(prolog, newprolog)
        return entry
