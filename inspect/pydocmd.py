# -*- coding: utf-8 -*-
"""Dumps module members to MD entries.
"""

import json
from . import pydump
from ..docpage import npdocs

__all__ = [
    'funcstomd', 'classtomd'
]


def apiobj(obj):
    obj.__module__ = 'docspyer'
    return obj


def modtomd(pymod, meta=None, npstyle=True, clsverbs=0) -> str:
    """Dumps functions and classes from a module in MD format.

    Parameters
    ----------
    pymod : module
        A python module to be documented.
    meta : dict = None
        Specifies JSON metadata of the output document.
    npstyle : bool = True
        Expects numpy style docstrings, if True.
        Otherwise, plain text format is used.
    clsverbs : int = 0
        Verbosity of classes from 0 to 2.

    Returns
    -------
    str
        The resulting MD document.

    """

    name = pymod.__name__
    docs = pymod.__doc__ or ''

    docs = npdocs.docasmd(docs)

    dumper = get_objdumper()
    doceditor = get_doceditor(npstyle)

    dumper.set_dumper(
        hostname=name, doceditor=doceditor, level=2, clsverbs=clsverbs
    )

    meta = get_metaformd(meta)

    heading = '# ' + name
    entries = pydump.docmod_with_dumper(pymod, dumper)

    parts = [
        meta, heading, docs, entries
    ]

    return '\n\n'.join(
        filter(len, parts)
    )


@apiobj
def funcstomd(*funcs, **settings) -> str:
    """Returns documentation of functions in MD.

    Parameters
    ----------
    funcs : tuple
        Functions to be documented.
    settings : dict
        Configuration settings (see below).

    Settings
    --------
    hostname : str = None
        Name of the functions holder.
    level : int = None
        Sets the level of functions headings.
    npstyle : bool = True
        Expects numpy style docstrings, if True.
        Otherwise, plain text format is used.

    """

    level = settings.get('level', None)
    npstyle = settings.get('npstyle', True)
    hostname = settings.get('hostname', None)

    dumper = get_objdumper()
    doceditor = get_doceditor(npstyle)

    dumper.set_dumper(
        hostname=hostname, doceditor=doceditor, level=level
    )

    parts = list(
        map(dumper.dumpobj, funcs)
    )

    return '\n\n'.join(parts)


@apiobj
def classtomd(pycls, **settings) -> str:
    """Returns a class documentation in MD.

    Parameters
    ----------
    pycls : type
        Class to be documented.
    settings : dict
        Configuration settings (see below).

    Settings
    --------
    hostname : str = None
        Name of the class holder.
    level : int = None
        Specifies the level of the class heading.
    npstyle : bool = True
        Expects numpy style docstrings, if True.
        Otherwise, plain text format is used.
    verbosity : int = 0
        Controls the class verbosity (0-2)
        regarding the methods headings.
    predicate : function = None
        Function that filters class methods.
        If None, only public methods with docs are retained.

    """

    level = settings.get('level', None)
    npstyle = settings.get('npstyle', True)
    hostname = settings.get('hostname', None)
    verbosity = settings.get('verbosity', 0)
    predicate = settings.get('predicate', None)

    dumper = get_objdumper()
    doceditor = get_doceditor(npstyle)

    config = {
        'hostname': hostname,
        'doceditor': doceditor,
        'clsverbs': verbosity,
        'level': level
    }

    dumper.set_dumper(**config)
    dumper.classdumper.set_predicate(predicate)

    return dumper.dumpobj(pycls)


def get_objdumper():

    dumpertypes = {
        'func': FuncDumperMD,
        'class': ClassDumperMD
    }

    return pydump.ObjectDumper(dumpertypes)


def get_doceditor(npstyle):
    if npstyle is True:
        return npdocs.docasmd
    return None


def get_metaformd(meta):

    if not meta:
        return ''

    meta = json.dumps(meta, indent=2)
    return f'<!--\n{meta}\n-->'


class DumperMD:
    """Base class for MD dumpers.
    """

    def __init__(self):
        self.level = None

    def build_header(self, name, signature):
        heading = self.make_heading(name)
        definition = self.make_definition(name, signature)
        return self.assemble(heading, definition)

    def make_heading(self, name):
        if self.level is None:
            return ''
        return HeadingMD().render(name, self.level)

    def make_definition(self, name, sign):
        name = self.edit_name_for_def(name)
        return self.render_defstr(name, sign)

    def render_defstr(self, name, sign):
        return PyDefstrMD().render(name, sign)

    def edit_name_for_def(self, name):
        """Final editing of the name in the definition block.
        """
        return name

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )

    def formatdoc(self, docs):
        return self.dump_as_codemd(docs)

    def dump_as_codemd(self, text):
        return f'```docstring\n{text}\n```'

    def format_content(self, content):
        """Final editing of the entry content before dumping. 
        """
        return content


class FuncDumperMD(DumperMD, pydump.FuncDumper):
    """Dumper for python functions in MD.
    """

    def edit_name_for_def(self, name):
        return self.add_hostname(name)


class ClassDumperMD(DumperMD, pydump.ClassDumper):
    """Dumper for python classes in MD.
    """

    def edit_name_for_def(self, name):
        name = self.add_hostname(name)
        return self.add_class_prefix(name)

    def add_class_prefix(self, name):
        return '<b><em>class</em></b> ' + name

    def format_method_entry(self, entry):
        return entry


class HeadingMD:
    """Makes an MD heading for a python object.
    """

    def render(self, name, level):
        name = self.format_name(name)
        return self.name_to_heading(name, level)

    def format_name(self, name):
        name = self.add_call_if_snake(name)
        return name

    def name_to_heading(self, name, level):
        if level == 0:
            return f'<b>{name}</b>'
        return '#'*level + ' ' + name

    def add_call_if_snake(self, name):
        if name.islower():
            return name + '()'
        return name


class PyDefstrMD:
    """Renders a definition of a python object in MD. 
    """

    def render(self, name, signature):
        content = self.make_content(name, signature)
        return self.dump_to_pretag(content)

    def make_content(self, name, sign):
        name = self.format_name(name)
        sign = self.format_sign(sign)
        return self.addstrings(name, sign)

    def format_name(self, name) -> str:
        return PyNameMD().render(name)

    def format_sign(self, signature) -> str:
        return PySignaMD().render(signature)

    def addstrings(self, *strs):
        return ''.join(strs)

    def dump_to_pretag(self, content):
        css = self.set_css_class()
        return f'<pre class="{css}">{content}</pre>'

    def set_css_class(self):
        return 'py-sign'


class PyNameMD:
    """Renders an object name in MD.
    """

    def render(self, name):
        basename = self.get_base_name(name)
        givenname = self.get_given_name(name)
        return self.assemble(basename, givenname)

    def get_given_name(self, name):
        _, _, givenname = name.rpartition('.')
        return self.make_bold(givenname)

    def get_base_name(self, name):
        basename, _, _ = name.rpartition('.')
        return basename

    def make_bold(self, name):
        return '<b>' + name + '</b>'

    def assemble(self, *parts):
        return '.'.join(
            filter(len, parts)
        )


class PySignaMD:
    """Renders a signature of a python object in MD.
    """

    def render(self, sign):
        sign = self.returns_to_em(sign)
        sign = self.arrow_to_rarr(sign)
        sign = self.format_params(sign)
        return sign

    def returns_to_em(self, sign):

        if '->' not in sign:
            return sign

        body, _, annot = sign.rpartition(' -> ')
        return body + ' -> ' + f'<em>{annot}</em>'

    def arrow_to_rarr(self, sign):
        return sign.replace(' -> ', ' → ')

    def format_params(self, sign):
        sign = self.true_false_as_span(sign)
        sign = self.self_cls_as_em(sign)
        sign = self.none_as_span(sign)
        return sign

    def none_as_span(self, sign):
        sign = sign.replace('=None', '=<span>None</span>')
        return sign

    def true_false_as_span(self, sign):
        sign = sign.replace('=True', '=<span>True</span>')
        sign = sign.replace('=False', '=<span>False</span>')
        return sign

    def self_cls_as_em(self, sign):
        sign = sign.replace('(self', '(<em>self</em>')
        sign = sign.replace('(cls', '(<em>cls</em>')
        return sign
