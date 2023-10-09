# -*- coding: utf-8 -*-
"""Records of python objects.
"""

from ..utils import namespace
from ..utils import deeptrees
from ..utils import treeastxt


class BaseRecord:
    """Base class for records of python objects.
    """

    def formatname(self, name) -> str:
        return name or ''

    def formatdocs(self, docs) -> str:

        if not docs:
            return ''

        if docs.count('\n') <= 1:
            return docs.strip()

        return docs.rstrip() + '\n'

    def print_trees(self, roots) -> str:

        views = list(
            map(treeastxt.dumptree_txt, roots)
        )

        return '\n\n'.join(views)

    def make_trees_from_namespace(self, name_to_names) -> list:
        return deeptrees.maketrees(name_to_names)

    def invert_name_to_names(self, name_to_names) -> dict:
        return namespace.invertmap(name_to_names)

    def list_names_as_tree(self, names, rootname) -> str:

        names_to_stub = {
            name: [] for name in names
        }

        return namespace.dumpnamespace(
            name_to_names=names_to_stub, rootname=rootname
        )

    def is_funcrec(self):
        return isinstance(self, FuncRecord)

    def is_classrec(self):
        return isinstance(self, ClassRecord)

    def is_modrec(self):
        return isinstance(self, ModuleRecord)

    def is_pyrec(self):
        return isinstance(
            self, (FuncRecord, ClassRecord, ModuleRecord)
        )


class FuncRecord(BaseRecord):
    """Represents a python function.

    Attributes
    ----------
    name : str
        Function name.
    docs : str
        Function docstring.
    signature : str
        Line with the function definition.
    calls : list[str]
        Call names from the function body.

    """

    def __init__(self):
        self.name = ''
        self.docs = ''
        self.signature = ''
        self.calls = []

    def dumpname(self) -> str:
        return self.formatname(self.name)

    def dumpdocs(self) -> str:
        return self.formatdocs(self.docs)

    def listcalls(self) -> list[str]:
        return list.copy(self.calls)

    def get_self_calls(self) -> list[str]:
        calls = self.fetch_self_calls()
        calls = self.remove_self_prefix(calls)
        return calls

    def fetch_self_calls(self) -> list[str]:
        def is_selfcall(call):
            return call.startswith('self.')
        return list(
            filter(is_selfcall, self.calls)
        )

    def remove_self_prefix(self, calls) -> list[str]:
        return [
            call.removeprefix('self.') for call in calls
        ]


class ClassRecord(BaseRecord):
    """Represents a python class.

    Attributes
    ----------
    name : str
        Class name.
    docs : str
        Class docstring.
    bases : list[str]
        Names of the parent classes.
    signature : str
        Line with the class definition.
    funcs : dict
        Namespace of class-level methods (name-to-record).

    """

    def __init__(self):
        self.name = ''
        self.docs = ''
        self.bases = []
        self.signature = ''
        self.funcs = {}

    def dumpname(self) -> str:
        return self.formatname(self.name)

    def dumpdocs(self) -> str:
        return self.formatdocs(self.docs)

    def dumpcalltrees(self) -> str:
        roots = self.makecalltrees()
        return self.print_trees(roots)

    def makecalltrees(self):
        func_to_calls = self.map_funcs_to_self_calls()
        return self.make_trees_from_namespace(func_to_calls)

    def map_funcs_to_self_calls(self) -> dict:

        def makeitem(funcrec):
            return (
                funcrec.name, funcrec.get_self_calls()
            )

        func_to_calls_items = map(
            makeitem, dict.values(self.funcs)
        )

        return dict(func_to_calls_items)

    def listfuncs(self) -> list[str]:
        return list(
            dict.keys(self.funcs)
        )


class ModuleRecord(BaseRecord):
    """Represents a python script (module).

    Attributes
    ----------
    name : str | None
        Module name.
    docs : str
        Module docstring.
    imports : list[str]
        Fully qualified names of imported objects.
    funcs : dict
        Namespace of module-level functions (name-to-record).
    classes : dict
        Namespace of module-level classes (name-to-record).

    """

    def __init__(self):
        self.name = ''
        self.docs = ''
        self.imports = []
        self.funcs = {}
        self.classes = {}

    def dumpname(self) -> str:
        return self.formatname(self.name)

    def dumpdocs(self) -> str:
        return self.formatdocs(self.docs)

    def dumpimports(self) -> str:
        return self.list_names_as_tree(
            self.imports, rootname='import'
        )

    def dumpcalltrees(self) -> str:
        roots = self.makecalltrees()
        return self.print_trees(roots)

    def dumpclasstrees(self) -> str:
        roots = self.makeclasstrees()
        return self.print_trees(roots)

    def makecalltrees(self) -> list:
        call_to_calls = self.map_calls_to_calls()
        call_to_calls = self.exclude_non_native_calls(call_to_calls)
        return self.make_trees_from_namespace(call_to_calls)

    def makeclasstrees(self) -> list:
        base_to_subclasses = self.map_bases_to_subclasses()
        return self.make_trees_from_namespace(base_to_subclasses)

    def map_bases_to_subclasses(self) -> dict:
        class_to_bases = self.map_classes_to_bases()
        return self.invert_name_to_names(class_to_bases)

    def map_calls_to_calls(self) -> dict:

        funcs_to_calls = self.map_funcs_to_calls()
        classes_to_stubs = self.map_classes_to_stubs()

        return {
            **funcs_to_calls, **classes_to_stubs
        }

    def map_clases_to_methods(self) -> dict:

        def makeitem(classrec):

            names = str(classrec.name)
            methods = list(dict.keys(classrec.funcs))

            if '__init__' in methods:
                methods.remove('__init__')

            return names, methods

        classrecs = dict.values(self.classes)

        return dict(
            map(makeitem, classrecs)
        )

    def map_classes_to_bases(self) -> dict:

        def makeitem(classrec):

            name = str(classrec.name)
            bases = list.copy(classrec.bases)

            if 'object' in bases:
                bases.remove('object')

            return name, bases

        classrecs = dict.values(self.classes)

        return dict(
            map(makeitem, classrecs)
        )

    def map_funcs_to_calls(self) -> dict:

        def makeitem(funcrec):
            return (
                funcrec.name, funcrec.listcalls()
            )

        funcrecs = dict.values(self.funcs)

        return dict(
            map(makeitem, funcrecs)
        )

    def map_classes_to_stubs(self) -> dict:
        return {
            classrec.name: [] for classrec in dict.values(self.classes)
        }

    def exclude_non_native_calls(self, call_to_calls) -> dict:
        return namespace.exclude_non_native_names(call_to_calls)
