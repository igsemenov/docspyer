# -*- coding: utf-8 -*-
"""Base dumpers for python functions and classes.
"""

import inspect


def docmembers(pymod, dumper) -> str:
    """Dumps functions and classes from a module.

    Parameters
    ----------
    pymod : module
        Python module to be documented.
    dumper : function
        Dumps function and classes.

    """

    members = getmembers(pymod)
    members = list(members)

    entries = list(
        map(dumper, members)
    )

    return '\n\n'.join(
        filter(len, entries)
    )


def getmembers(module):
    """Selects functions and classes from the module.
    """

    for val in module.__dict__.values():
        if inspect.isfunction(val):
            yield val
        if inspect.isclass(val):
            yield val


class Dumper:
    """Base class for dumpers.
    """

    def set_doceditor_if_any(self, doceditor):
        if doceditor is None:
            return
        setattr(self, 'doceditor', doceditor)

    def dumpobj(self, obj):
        header = self.make_header(obj)
        content = self.make_content(obj)
        return self.assemble(header, content)

    def make_header(self, obj):
        name = self.dumpname(obj)
        signature = self.dumpsignature(obj)
        return self.format_header(name, signature)

    def format_header(self, name, signature):
        return name + signature

    def make_content(self, obj):
        return obj.__doc__ or ''

    # Dumpers

    def dumpname(self, obj) -> str:
        return obj.__module__ + '.' + obj.__qualname__

    def dumpdocs(self, obj) -> str:

        docs = self.get_clean_docs(obj)

        if not docs:
            return ''

        res = self.apply_doceditor_if_any(docs)
        if res is not None:
            return res

        return self.dump_docs_as_text_otherwise(docs)

    def dumpsignature(self, obj):

        getter = self.getsignature
        formatter = self.formatsignature

        signature = getter(obj)
        return formatter(signature)

    # Getters

    def get_clean_docs(self, obj):

        getter = self.getdocs
        formatter = self.formatdocs

        docs = getter(obj)
        return formatter(docs)

    def getdocs(self, obj):
        return inspect.getdoc(obj) or ''

    def getsignature(self, obj) -> str:
        return str(
            inspect.signature(obj)
        )

    # Formatters

    def formatdocs(self, docs):

        if not docs:
            return ''

        if docs.count('\n') <= 1:
            return docs.strip()

        return docs.rstrip() + '\n'

    def formatsignature(self, signature) -> str:
        return signature

    # Utils

    def apply_doceditor_if_any(self, docs):
        if hasattr(self, 'doceditor'):
            return getattr(self, 'doceditor')(docs)
        return None

    def dump_docs_as_text_otherwise(self, docs):
        return docs

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )


class FuncDumper(Dumper):
    """Base dumper for functions.
    """

    def make_content(self, obj):
        return self.dumpdocs(obj)

    def format_content(self, docs):
        return docs


class ClassDumper(Dumper):
    """Base dumper for classes.
    """

    def set_funcsdumper(self, funcsdumper):
        setattr(self, 'funcsdumper', funcsdumper)

    def make_content(self, obj):
        docs = self.dumpdocs(obj)
        funcs = self.dumpmethods(obj)
        return self.format_content(docs, funcs)

    def format_content(self, docs, funcs):
        return '\n\n'.join(
            filter(len, [docs, funcs])
        )

    def dumpmethods(self, obj) -> str:
        if self.break_if_no_funcsdumper():
            return ''
        return self.run_methodsdumper_otherwise(obj)

    def break_if_no_funcsdumper(self) -> bool:
        return not hasattr(self, 'funcsdumper')

    def run_methodsdumper_otherwise(self, obj):
        return getattr(self, 'methodsdumper')(obj)

    def methodsdumper(self, obj) -> list[str]:

        funcs = self.select_methods(obj)

        entries = self.run_funcsdumper(funcs)
        entries = self.funcs_to_methods(entries)
        return self.assemble(*entries)

    def run_funcsdumper(self, funcs) -> list[str]:

        funcsdumper = getattr(self, 'funcsdumper').dumpobj

        return list(
            map(funcsdumper, funcs)
        )

    def funcs_to_methods(self, entries):
        return list(
            map(self.func_entry_to_method, entries)
        )

    def func_entry_to_method(self, entry):
        return entry

    def select_methods(self, obj):

        funcsfetcher = self.fetchfuncs
        funcs = funcsfetcher(obj)

        return list(
            filter(self.hasdocs, funcs)
        )

    def hasdocs(self, obj):
        return bool(obj.__doc__)

    def fetchfuncs(self, obj):

        def getfunc(obj):
            if inspect.isfunction(obj):
                return obj
            if inspect.ismethod(obj):
                return obj.__func__
            return None

        members = obj.__dict__.values()

        prefetch = list(
            map(getfunc, members)
        )

        return list(
            filter(bool, prefetch)
        )
