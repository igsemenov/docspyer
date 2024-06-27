# -*- coding: utf-8 -*-
"""Base dumpers for functions, classes and modules.
"""

from abc import ABC
from abc import abstractmethod
import inspect

__all__ = [
    'classfuncs'
]


def apiobj(obj):
    obj.__module__ = 'docspyer'
    return obj


@apiobj
def classfuncs(pycls, predicate=None) -> list:
    """Fetches methods from a class.

    Parameters
    ----------
    pycls : type
        Class to be inspected.
    predicate : function = None
        Function that filters class methods.
        If None, only public methods with docs are retained.

    Returns
    -------
    list
        List with the selected methods.

    """
    explorer = ClassExplorer()
    return explorer.getmethods(pycls, predicate)


def docmod_with_dumper(pymod, dumper) -> str:
    """Dumps functions and classes from a module.

    Parameters
    ----------
    pymod : module
        Python module to be documented.
    dumper : ObjectDumper
        Runtime dumper for module members.

    """

    members = get_mod_members(pymod)
    members = filter_mod_members(members)

    text = run_dumper(members, dumper)
    return text


def run_dumper(members, dumper) -> str:

    entries = list(
        map(dumper.dumpobj, members)
    )

    return '\n\n'.join(
        filter(len, entries)
    )


def get_mod_members(module):
    """Selects functions and classes from the module.
    """

    for val in module.__dict__.values():
        if inspect.isfunction(val):
            yield val
        if inspect.isclass(val):
            yield val


def filter_mod_members(members) -> list:

    def is_member(obj):
        return bool(obj.__doc__)

    return list(
        filter(is_member, members)
    )


class Dumper(ABC):
    """Base dumper for python objects.

    Attributes
    ----------
    level : int
        Object level in a local hierarchy.
    hostname : str
        Used as the prefix before the given name.
    doceditor : function
        Performs final editing of a docstring before dumping.
        Can be overridden by the external editor, otherwise 
        the local implementation is used.

    """

    def __init__(self):
        self.level = None
        self.hostname = None
        self.doceditor = None

    def set_dumper(self, hostname=None, doceditor=None, level=None):
        """Must always be called before using the dumper.
        """
        self.set_level(level)
        self.set_hostname(hostname)
        self.set_doceditor(doceditor)

    def set_level(self, level):
        self.level = level

    def set_hostname(self, hostname):
        self.hostname = hostname or ''

    def set_doceditor(self, doceditor):
        self.doceditor = doceditor or self.formatdoc

    def dumpobj(self, obj) -> str:
        """Top-level method that dumps an object.
        """
        header = self.make_header(obj)
        content = self.make_content(obj)
        content = self.format_content(content)
        return self.assemble(header, content)

    def make_header(self, obj):
        name = self.dumpname(obj)
        signature = self.dumpsignature(obj)
        return self.build_header(name, signature)

    def make_content(self, obj):
        docs = self.dumpdocs(obj)
        extra = self.get_extra_content(obj)
        return self.assemble(docs, extra)

    def dumpname(self, obj) -> str:
        return obj.__name__

    def dumpsignature(self, obj):
        return SignPrinter().dumpsign(obj)

    def dumpdocs(self, obj) -> str:
        docs = self.run_docsprinter(obj)
        return self.run_doceditor(docs)

    def run_docsprinter(self, obj):
        return DocsPrinter().dumpdocs(obj)

    def run_doceditor(self, docs):
        doceditor = self.doceditor
        return doceditor(docs)

    @abstractmethod
    def build_header(self, name, signature) -> str:
        """Returns the final version of the header.
        """

    @abstractmethod
    def formatdoc(self, docs) -> str:
        """Internal formatter of docstrings.
        """

    @abstractmethod
    def get_extra_content(self, obj) -> str:
        """Returns extra content for the object entry.
        """
        return ''

    @abstractmethod
    def format_content(self, text) -> str:
        """Final editing of the entry content before dumping.
        """
        return text

    def add_hostname(self, name):
        if not self.hostname:
            return name
        return self.hostname + '.' + name

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )


class FuncDumper(Dumper):
    """Base dumper for functions.
    """

    def __init__(self):
        super().__init__()
        self.ismethod = False

    def mark_as_method(self):
        self.ismethod = True

    def get_extra_content(self, obj):
        return self.empty_string()

    def empty_string(self):
        return ''


class ClassDumper(Dumper):
    """Base dumper for classes.
    """

    def __init__(self):
        super().__init__()
        self.predicate = None
        self.funcdumper = None

    def set_predicate(self, predicate):
        self.predicate = predicate

    def set_funcdumper(self, funcdumper):
        self.funcdumper = funcdumper

    def get_extra_content(self, obj):
        entries = self.get_methods_entries(obj)
        entries = self.format_entries(entries)
        return self.assemble(*entries)

    def get_methods_entries(self, obj) -> list[str]:

        methods = self.getmethods(obj)

        if not methods:
            return ''

        return self.run_funcdumper(methods)

    def getmethods(self, obj) -> list:
        return ClassExplorer().getmethods(obj, predicate=self.predicate)

    def run_funcdumper(self, methods) -> list[str]:

        funcdumper = self.funcdumper

        return list(
            map(funcdumper.dumpobj, methods)
        )

    def format_entries(self, entries):
        return list(
            map(self.format_method_entry, entries)
        )

    @abstractmethod
    def format_method_entry(self, entry):
        """Final formatting of the method entry before dumping.
        """


class ObjectDumper:
    """Runtime dumper for module members.

    Parameters
    ----------
    dumpertypes : dict
        Contains types of dumpers for functions and classes.        

    """

    def __init__(self, dumpertypes):

        self.dumpertypes: dict = dumpertypes

        self.funcdumper = None
        self.classdumper = None

    def dumpobj(self, obj) -> str:
        if inspect.isfunction(obj):
            return self.functomd(obj)
        if inspect.isclass(obj):
            return self.classtomd(obj)
        return ''

    def set_dumper(self, **config):
        """Must be called before using the dumper.
        """

        hostname = config.get('hostname', None)
        doceditor = config.get('doceditor', None)
        level = config.get('level', None)
        clsverbs = config.get('clsverbs', 0)

        self.set_funcdumper(hostname, doceditor, level)
        self.set_classdumper(hostname, doceditor, level, clsverbs)

    def set_funcdumper(self, hostname, doceditor, level):

        funcdumper = self.dumpertypes['func']()

        funcdumper.set_dumper(
            hostname=hostname, doceditor=doceditor, level=level
        )

        self.funcdumper = funcdumper

    def set_classdumper(self, hostname, doceditor, level, clsverbs):

        classdumper = self.dumpertypes['class']()
        methodsdumper = self.dumpertypes['func']()

        classdumper.set_dumper(
            hostname=hostname, doceditor=doceditor, level=level
        )

        level = self.set_verbosity(level, clsverbs)

        methodsdumper.set_dumper(
            hostname=None, doceditor=doceditor, level=level
        )

        methodsdumper.mark_as_method()

        classdumper.set_predicate(None)
        classdumper.set_funcdumper(methodsdumper)

        self.classdumper = classdumper

    def set_verbosity(self, level, clsverbs):
        if clsverbs == 0:
            return None
        if clsverbs == 1:
            return 0
        return level+1 if level else None

    def functomd(self, pyfunc):
        dumper = self.funcdumper
        return dumper.dumpobj(pyfunc)

    def classtomd(self, pycls):
        dumper = self.classdumper
        dumper.funcdumper.hostname = pycls.__name__
        return dumper.dumpobj(pycls)


class ClassExplorer:
    """Extract methods from a python class.

    Local search:

        fetch_methods()
         └─ only_locals()

    Deep search:

        fetch_methods()
         └─ deep_search()

    """

    def getmethods(self, pycls, predicate=None) -> list:

        methods = self.fetch_methods(pycls)
        methods = self.select_relevant(methods, predicate)

        return methods

    def fetch_methods(self, pycls) -> list:
        members = self.only_locals(pycls)
        members = self.unfold_clsmethods(members)
        return members

    def only_locals(self, pycls) -> list:

        members = list(
            vars(pycls).values()
        )

        return list(
            filter(self.ismethod, members)
        )

    def deep_search(self, pycls) -> list:

        members = inspect.getmembers(
            pycls, predicate=self.ismethod
        )

        asdict = dict(members)

        return list(
            asdict.values()
        )

    def unfold_clsmethods(self, members):
        def getfunc(func):
            if inspect.isfunction(func):
                return func
            if inspect.ismethod(func):
                return func.__func__
            return func
        return list(
            map(getfunc, members)
        )

    def select_relevant(self, methods, predicate) -> list:

        res = self.run_predicate_if_any(methods, predicate)

        if res is not None:
            return res

        return self.run_default_otherwise(methods)

    def run_predicate_if_any(self, methods, predicate):
        if predicate is None:
            return None
        return list(
            filter(predicate, methods)
        )

    def run_default_otherwise(self, methods):
        methods = self.retain_public(methods)
        methods = self.retain_with_docs(methods)
        return methods

    def ismethod(self, obj):
        if inspect.isfunction(obj):
            return True
        if inspect.ismethod(obj):
            return True
        return False

    def retain_public(self, methods) -> list:
        def is_public(obj):
            return not obj.__name__.startswith('_')
        return list(
            filter(is_public, methods)
        )

    def retain_with_docs(self, methods) -> list:
        return list(
            filter(self.hasdocs_local, methods)
        )

    def hasdocs_deep(self, obj) -> bool:
        if inspect.getdoc(obj):
            return True
        return False

    def hasdocs_local(self, obj) -> bool:
        if obj.__doc__ is None:
            return False
        return bool(obj.__doc__)


class SignPrinter:
    """Dumps the signature of a callable.
    """

    def dumpsign(self, obj) -> str:
        obj = self.unfold_object(obj)
        return self.render_signature(obj)

    def unfold_object(self, obj):
        return self.func_from_clsmethod(obj)

    def func_from_clsmethod(self, obj) -> str:
        if inspect.ismethod(obj):
            return obj.__func__
        return obj

    def render_signature(self, obj):
        return str(
            inspect.signature(obj)
        )


class DocsPrinter:
    """Returns a clean docstring of a python object.
    """

    def dumpdocs(self, obj):
        docs = self.fetchdocs(obj)
        return self.cleandocs(docs)

    def cleandocs(self, docs):

        if not docs:
            return ''

        if docs.count('\n') <= 1:
            return docs.strip()
        return docs.rstrip() + '\n'

    def fetchdocs(self, obj):
        return inspect.getdoc(obj) or ''
