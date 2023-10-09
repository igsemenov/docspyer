# -*- coding: utf-8 -*-
"""Generates MD reports for python scripts.
"""

import textwrap
from . import pyparser


def makereport(source, name) -> str:
    """Generates an MD report on given python script (module).

    Parameters
    ----------
    source : str
        Python script to be examined.
    name : str
        User-defined name of the script.

    Returns
    -------
    str
        The resulting report in MD.

    """
    modrec = parse_script(source, name)
    return run_reporter(modrec)


def parse_script(source, name):
    return run_pyparser(source, name)


def run_pyparser(source, name):
    return pyparser.parsescript(source, name)


def run_reporter(modrec):
    module_reporter = ScriptReporter()
    return module_reporter.make_report(modrec)


class Reporter:
    """Base class for reporters.
    """

    def make_report(self, record) -> str:

        heading = self.make_heading(record)
        content = self.make_content(record)

        if not content:
            return ''

        return self.assemble(heading, content)

    def make_heading(self, record):
        return record.name

    def make_content(self, record):
        return record.docs

    # Getters

    def get_docstr_from_record(self, pyrec):
        return pyrec.dumpdocs()

    def get_calltrees_from_record(self, pyrec):
        return pyrec.dumpcalltrees()

    def get_imports_from_record(self, pyrec):
        return pyrec.dumpimports()

    def get_classtrees_from_record(self, pyrec):
        return pyrec.dumpclasstrees()

    # Dumpers

    def dump_docstr(self, pyrec) -> str:

        docstr = self.get_docstr_from_record(pyrec)
        docstr = self.indent_to_escape_md(docstr)

        return self.dump_to_labeled_text_block(
            text=docstr, label='docstring'
        )

    def indent_to_escape_md(self, text):
        return textwrap.indent(text, prefix=' ')

    def dump_calltrees(self, pyrec) -> str:

        calltrees = self.get_calltrees_from_record(pyrec)

        return self.dump_to_labeled_text_block(
            text=calltrees, label='call-trees'
        )

    def dump_imports(self, modrec) -> str:

        imports = self.get_imports_from_record(modrec)

        return self.dump_to_labeled_text_block(
            text=imports, label='imports-view'
        )

    def dump_classtrees(self, modrec) -> str:

        classtrees = self.get_classtrees_from_record(modrec)

        return self.dump_to_labeled_text_block(
            text=classtrees, label='class-trees'
        )

    # Utils

    def assemble(self, *parts) -> str:
        return '\n\n'.join(
            filter(len, parts)
        )

    def empty_heading(self):
        return ''

    def first_level_heading(self, text):
        return '# ' + text

    def second_level_heading(self, text):
        return '## ' + text

    def dump_to_labeled_text_block(self, text, label) -> str:
        if not text:
            return ''
        return f'```{label}\n{text}\n```'


class ScriptReporter(Reporter):
    """Generates a report on a python script.

    A report includes:

    - Module overview (top-level).
    - Reports on most important classes. 

    """

    def __init__(self):
        self.set_module_reporter()
        self.set_class_reporter()

    def set_class_reporter(self):
        self.class_reporter = ClassReporter()

    def set_module_reporter(self):
        self.module_reporter = ModuleReporter()

    def make_heading(self, record) -> str:
        return self.empty_heading()

    def make_content(self, record) -> str:

        modrec = record

        module_report = self.review_module(modrec)
        class_reports = self.review_classes(modrec)

        return self.assemble(
            module_report, class_reports
        )

    def review_module(self, modrec) -> str:
        reviewer = self.module_reporter
        return reviewer.make_report(modrec)

    def review_classes(self, modrec) -> str:
        entries = self.get_class_reports(modrec)
        return self.assemble(*entries)

    def get_class_reports(self, modrec):

        reporter = self.class_reporter

        return map(
            reporter.make_report, modrec.classes.values()
        )


class ModuleReporter(Reporter):
    """Generates a report on a module (top-level).
    """

    def make_heading(self, record) -> str:
        return self.first_level_heading(record.name)

    def make_content(self, record) -> str:

        modrec = record

        docstr = self.dump_docstr(modrec)
        imports = self.dump_imports(modrec)
        calltrees = self.dump_calltrees(modrec)
        classtrees = self.dump_classtrees(modrec)

        return self.assemble(
            docstr, imports, calltrees, classtrees
        )


class ClassReporter(Reporter):
    """Generates a report on a class.
    """

    def make_heading(self, record) -> str:
        return self.second_level_heading(record.name)

    def make_content(self, record) -> str:

        classrec = record

        docstr = self.dump_docstr(classrec)
        calltrees = self.dump_calltrees(classrec)

        return self.assemble(docstr, calltrees)
