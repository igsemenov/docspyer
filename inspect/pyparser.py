# -*- coding: utf-8 -*-
"""Parser of python scripts.
"""

import re
import ast

from . import pyrecords


def parsescript(source, scriptname=None):
    """Performs structural analysis of a python script (module).

    Parameters
    ----------
    source : str
        A python script to be examined.
    scriptname : str
        User-defined name of the script (optional).

    Returns
    -------
    ModuleRecord
        Object that describes imports, functions and classes.

    """
    astmodule = parse_via_ast_parser(source)
    modrec = run_module_recorder(astmodule, scriptname)
    return modrec


def parse_via_ast_parser(source):
    return ast.parse(source)


def run_module_recorder(astmodule, scriptname):
    recorder = ModuleRecorder()
    return recorder.make_record(astmodule, scriptname)


class BaseRecorder:
    """Base class for object recorders.
    """

    def get_name(self, astnode) -> str:
        return astnode.name

    def get_docs(self, astnode) -> str:
        return ast.get_docstring(astnode) or ''

    def get_signature(self, astnode) -> str:
        barenode = self.remove_node_body(astnode)
        return self.unparse_node(barenode)

    def fetch_funcs(self, astnode):
        return self.fetch_nodes_by_type(
            astnode, typeinfo=ast.FunctionDef
        )

    def fetch_classes(self, astnode):
        return self.fetch_nodes_by_type(
            astnode, typeinfo=ast.ClassDef
        )

    def fetch_imports(self, astnode):
        return self.fetch_nodes_by_type(
            astnode, typeinfo=(ast.Import, ast.ImportFrom)
        )

    def unparse_node(self, astnode):
        return ast.unparse(astnode)

    def fetch_nodes_by_type(self, astnode, typeinfo):
        def is_of_type(node):
            return isinstance(node, typeinfo)
        return list(
            filter(is_of_type, astnode.body)
        )

    def remove_node_body(self, astnode):
        newparams = vars(astnode) | {'body': []}
        return astnode.__class__(**newparams)

    def make_namespace_from_records(self, records):
        return {
            record.name: record for record in records
        }


class FuncRecorder(BaseRecorder):

    NodeType = ast.FunctionDef

    def __init__(self):
        self.set_call_parser()

    def set_call_parser(self):
        self.call_parser = CallParser()

    def make_record(self, astfunc):

        record = pyrecords.FuncRecord()

        record.name = self.get_name(astfunc)
        record.docs = self.get_docs(astfunc)
        record.signature = self.get_signature(astfunc)
        record.calls = self.get_calls(astfunc)

        return record

    def get_calls(self, astfunc) -> list[str]:
        callexprs = self.get_callexprs(astfunc)
        return self.fetch_first_calls(callexprs)

    def get_callexprs(self, astfunc) -> list[str]:
        astcalls = self.fetch_call_nodes(astfunc)
        callexprs = self.unparse_call_nodes(astcalls)
        return callexprs

    def fetch_call_nodes(self, astfunc) -> list:
        def is_call(node):
            return isinstance(node, ast.Call)
        return list(
            filter(is_call, ast.walk(astfunc))
        )

    def unparse_call_nodes(self, astcalls) -> list[str]:
        return [
            ast.unparse(call) for call in astcalls
        ]

    def fetch_first_calls(self, callexprs) -> list[str]:

        fetcher = self.call_parser.fetch_first_call_name

        return list(
            map(fetcher, callexprs)
        )


class ClassRecorder(BaseRecorder):

    NodeType = ast.ClassDef

    def __init__(self):
        self.set_func_recorder()

    def set_func_recorder(self):
        self.func_recorder = FuncRecorder()

    def make_record(self, astclass):

        record = pyrecords.ClassRecord()

        record.name = self.get_name(astclass)
        record.docs = self.get_docs(astclass)
        record.bases = self.get_bases(astclass)
        record.signature = self.get_signature(astclass)
        record.funcs = self.get_funcs(astclass)

        return record

    def get_bases(self, astclass) -> list[str]:
        return [
            ast.unparse(base) for base in astclass.bases
        ]

    def get_funcs(self, astnode) -> dict:
        funcnodes = self.fetch_funcs(astnode)
        funcrecs = self.record_funcs(funcnodes)
        return self.make_namespace_from_records(funcrecs)

    def record_funcs(self, astfuncs):

        recorder = self.func_recorder.make_record

        return list(
            map(recorder, astfuncs)
        )


class ModuleRecorder(BaseRecorder):

    def __init__(self):
        self.set_func_recorder()
        self.set_class_recorder()
        self.set_imports_recorder()

    def set_func_recorder(self):
        self.func_recorder = FuncRecorder()

    def set_class_recorder(self):
        self.class_recorder = ClassRecorder()

    def set_imports_recorder(self):
        self.imports_recorder = ImportsRecorder()

    def set_module_name(self, modrec, modname):
        modrec.name = modname

    def make_record(self, astmodule, scriptname):

        record = pyrecords.ModuleRecord()

        self.set_module_name(record, scriptname)

        record.docs = self.get_docs(astmodule)
        record.funcs = self.get_funcs(astmodule)
        record.classes = self.get_classes(astmodule)
        record.imports = self.get_imports(astmodule)

        return record

    def get_funcs(self, astnode) -> dict:
        funcnodes = self.fetch_funcs(astnode)
        funcrecs = self.record_funcs(funcnodes)
        return self.make_namespace_from_records(funcrecs)

    def get_classes(self, astnode) -> dict:
        classnodes = self.fetch_classes(astnode)
        classrecs = self.record_classes(classnodes)
        return self.make_namespace_from_records(classrecs)

    def get_imports(self, astnode) -> list:
        imports = self.fetch_imports(astnode)
        return self.record_imports(imports)

    def record_funcs(self, astfuncs):

        recorder = self.func_recorder.make_record

        return list(
            map(recorder, astfuncs)
        )

    def record_classes(self, astclasses):

        recorder = self.class_recorder.make_record

        return list(
            map(recorder, astclasses)
        )

    def record_imports(self, astimports):
        recorder = self.imports_recorder.make_record
        return recorder(astimports)


class ImportsRecorder:

    def make_record(self, astimports) -> list[str]:
        importnames = []
        for astimport in astimports:
            importnames.extend(
                self.get_import_names(astimport)
            )
        return importnames

    def get_import_names(self, astimport) -> list:

        modname = self.get_module_name(astimport)

        names = list(
            map(self.get_alias_name, astimport.names)
        )

        if not modname:
            return names

        names = [
            modname + name for name in names
        ]

        return names

    def get_alias_name(self, alias) -> str:
        return alias.asname or alias.name

    def get_module_name(self, astimport) -> str:
        if not hasattr(astimport, 'module'):
            return str()
        if astimport.module is None:
            return '.'*astimport.level
        return '.'*astimport.level + astimport.module + '.'


class CallParser:
    """Parser of complex call expressions.
    """

    re_call = '[.\w]{1,}\('
    re_map = '(map|filter|[.\w]{0,}starmap)\('

    def fetch_first_call_name(self, callexpr) -> str:

        result = self.try_to_parse_as_map(callexpr)
        if result is not None:
            return result

        result = self.try_to_parse_as_call(callexpr)
        if result is not None:
            return result

        return self.return_empty_name_otherwise()

    def try_to_parse_as_map(self, callexpr) -> str | None:
        if re.match(self.re_map, callexpr):
            return self.fetch_callname_from_map(callexpr)
        return None

    def try_to_parse_as_call(self, callexpr) -> str | None:
        if re.match(self.re_call, callexpr):
            return self.fetch_callname_from_call(callexpr)
        return None

    def fetch_callname_from_map(self, callexpr) -> str:
        _, _, callexpr = callexpr.partition('(')
        callname, _, _ = callexpr.partition(',')
        return callname.strip()

    def fetch_callname_from_call(self, callexpr) -> str:
        callname, _, _ = callexpr.partition('(')
        return callname.strip()

    def return_empty_name_otherwise(self):
        return ''
