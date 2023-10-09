# -*- coding: utf-8 -*-
"""Outlines a group of python scripts.
"""

import re
from . import pyparser
from ..utils import namespace
from ..utils import tableasmd


def makeoutline(scripts) -> str:
    """Outlines a group of scripts.

    Parameters
    ----------
    scripts : Scripts
        Object that describes the scripts.

    Returns
    -------
    str
        The resulting outline in MD.

    """
    outliner = OutlineMaker()
    return outliner.make_outline(scripts)


class OutlineMaker:

    def make_outline(self, scripts) -> str:
        sketches = self.create_sketches(scripts)
        return self.outline_sketches(sketches)

    def create_sketches(self, scripts) -> list:

        sketcher = ScriptSketcher()
        scriptrecs = scripts.scripts.values()

        return list(
            map(sketcher.make_sketch, scriptrecs)
        )

    def outline_sketches(self, sketches):

        importsview = self.render_imports_view(sketches)
        modulestable = self.render_modules_table(sketches)

        return self.assemble(
            modulestable, importsview
        )

    def render_modules_table(self, scripts):
        table = ModulesTablePrinter().dumptable(scripts)
        return self.add_heading_table(table)

    def render_imports_view(self, scripts):
        view = ImportsViewPrinter().dumpview(scripts)
        return self.add_heading_imports(view)

    def add_heading_table(self, table):
        if not table:
            return ''
        return '## Annotations\n\n' + table

    def add_heading_imports(self, view):
        if not view:
            return ''
        return '## Imports\n\n' + view

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )


class ModulesTablePrinter:
    """Creates an overview table for scripts sketches.
    """

    def __init__(self):
        self.set_annotator()

    def set_annotator(self):
        self.annotator = Annotator()

    def dumptable(self, scripts) -> str:
        """Returns an overview table as a string.

        Parameters
        ----------
        scripts : Iterable[ScriptSketch]
            Sequence of scripts sketches.            

        """

        if not scripts:
            return ''

        columns = self.format_data(scripts)
        table = self.print_table(columns)

        return table

    def format_data(self, scripts):

        names = self.get_formated_names(scripts)
        annotations = self.get_annotations(scripts)

        first_column = [
            'Module', *names
        ]

        second_column = [
            'Description', *annotations
        ]

        return [
            first_column, second_column
        ]

    def get_formated_names(self, scripts):

        def formatname(name):
            return f'<b>{name}</b>'

        names = [
            script.name for script in scripts
        ]

        return list(
            map(formatname, names)
        )

    def get_annotations(self, scripts):

        annotator = self.annotator.getannotation

        return [
            annotator(script.docs) for script in scripts
        ]

    def print_table(self, columns):
        return tableasmd.maketablemd(columns)


class ImportsViewPrinter:

    def dumpview(self, scripts) -> str:

        imports_views = self.print_imports_for_scripts(scripts)

        content = self.dump_to_labeled_text_block(
            text=imports_views, label='imports-view'
        )

        return content

    def print_imports_for_scripts(self, scripts):

        printer = self.print_script_imports

        views = list(
            map(printer, scripts)
        )

        return '\n\n'.join(
            filter(len, views)
        )

    def print_script_imports(self, script):

        imports = self.map_imports_to_stubs(script)

        return self.print_namespace(
            name_to_names=imports, rootname=script.name
        )

    def map_imports_to_stubs(self, script):
        return {
            name: [] for name in script.imports
        }

    def print_namespace(self, name_to_names, rootname):
        return namespace.dumpnamespace(name_to_names, rootname)

    def dump_to_labeled_text_block(self, text, label) -> str:
        if not text:
            return ''
        return f'```{label}\n{text}\n```'


class ScriptSketch:

    def __init__(self, name, docs, imports):

        self.name = name
        self.docs = docs
        self.imports = imports


class ScriptSketcher:

    def make_sketch(self, script):

        header = self.fetch_header(script.source)
        record = self.parse_header(header)

        name = script.name
        docs = record.docs or ''
        imports = record.imports

        return ScriptSketch(
            name, docs, imports
        )

    def fetch_header(self, pytext):
        header_start = self.find_first_def_or_class(pytext)
        return pytext[0:header_start]

    def parse_header(self, header):
        return pyparser.parsescript(header)

    def find_first_def_or_class(self, pytext) -> int:

        matchobj = re.search(
            '^(@\w|def\s|class\s)', pytext, flags=re.MULTILINE
        )

        if matchobj is None:
            return len(pytext)

        return matchobj.start()


class Annotator:

    PY_LINE_LIMIT = 79
    NO_ANNOTATION = 'Failed to get annotation.'

    def getannotation(self, text):

        text = text.strip()

        if not text:
            return self.NO_ANNOTATION

        firstline = self.get_first_line(text)
        firstsentence = self.get_first_sentence(firstline)

        if not firstsentence:
            return self.NO_ANNOTATION

        line_length_is_ok = self.check_line_length(firstline)

        if not line_length_is_ok:
            return self.NO_ANNOTATION

        return firstsentence + '.'

    def check_line_length(self, line) -> bool:
        return len(line) < self.PY_LINE_LIMIT

    def get_first_line(self, text):
        text = text.rstrip() + '\n'
        firstline, *_ = text.splitlines()
        return firstline

    def get_first_sentence(self, text):
        firstsentence, _, _ = str.rpartition(text + ' ', '. ')
        return firstsentence
