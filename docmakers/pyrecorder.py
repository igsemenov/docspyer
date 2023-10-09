# -*- coding: utf-8 -*-
"""Creates MD documentation for a group of python modules.
"""

import os
import textwrap

from . import utils
from ..utils import contents
from ..inspect import pyoutline, pydocmd

__all__ = [
    'docmodules'
]

apiobj = utils.apiobj


@apiobj
def docmodules(modules, docpath, hostname=None):
    """Creates MD documentation for a group of python modules.

    Parameters
    ----------
    modules : list
        List of python modules (objects)
    docpath : str
        Path where to place the output files.
    hostname : str = None
        Name of the modules holder (package, namespace, etc.)
        to set the webtitles of the output files.

    """
    recorder = ModulesRecorder()
    recorder.doc_modules(modules, docpath, hostname)


class ModulesRecorder:
    """Makes MD documentation for a group of python modules.
    """

    def __init__(self):
        self._docpath = None
        self._hostname = None

    def doc_modules(self, modules, docpath, hostname=None):

        self._docpath = docpath
        self._hostname = hostname or ''

        sources = self.make_sources(modules)
        outline = self.make_outline(sources, modules)

        self.dump_files(outline, sources)

    def make_outline(self, sources, modules):
        table = self.make_table(modules)
        jointtoc = self.make_reference(sources)
        return self.run_outliner(table, jointtoc)

    def run_outliner(self, table, jointtoc):
        return ModulesOutlineMaker().make_outline(
            table, jointtoc, hostname=self._hostname
        )

    def make_table(self, modules):
        return ModulesTableMaker().make_table(modules)

    def make_reference(self, sources):
        return contents.makemultitoc(
            sources, level=3
        )
        # return contents.makemonotoc(sources)

    def make_sources(self, modules) -> dict:
        return dict(
            self.modules_to_items(modules)
        )

    def modules_to_items(self, modules):

        item_maker = self.module_to_item

        return list(
            map(item_maker, modules)
        )

    def module_to_item(self, pymod):
        name = self.getname(pymod)
        text = self.module_to_md(pymod)
        return name, text

    def getname(self, pymod):
        return pymod.__name__

    def module_to_md(self, pymod):
        return pydocmd.modtomd(
            pymod, meta=self.specify_module_meta(pymod)
        )

    def specify_module_meta(self, pymod):
        return {
            "webtitle": self.make_module_webtitle(pymod)
        }

    def make_module_webtitle(self, pymod):
        if not self._hostname:
            return pymod.__name__
        return pymod.__name__ + f' — {self._hostname} documentation'

    def dump_files(self, outline, sources):

        dumper = self.dump_file

        self.dump_outline(outline, dumper)
        self.dump_sources(sources, dumper)

    def dump_outline(self, outline, dumper):
        dumper(
            name='modules', content=outline
        )

    def dump_sources(self, sources, dumper):
        for name, content in sources.items():
            dumper(name, content)

    def dump_file(self, name, content):

        filepath = os.path.join(
            self._docpath, name + '.md'
        )

        utils.dump_file(filepath, content)


class ModulesOutlineMaker:
    """Creates an outline — `modules.md`.
    """

    META = """
    <!--
    {
      "webtitle": "WEBTITLE",
      "doctitle": "Modules"
    }
    -->
    """

    def make_outline(self, table, jointtoc, hostname):

        meta = self.get_meta(hostname)
        table = self.render_table(table)
        reference = self.render_reference(jointtoc)

        return self.assemble(
            meta, table, reference
        )

    def render_table(self, table):
        return self.add_table_heading(table)

    def render_reference(self, jointtoc):
        return self.add_reference_heading(jointtoc)

    def add_table_heading(self, table):
        return '## Annotations\n\n' + table

    def add_reference_heading(self, jointtoc):
        return '## Reference\n\n' + jointtoc

    def get_meta(self, hostname):
        webtitle = self.make_webtitle(hostname)
        meta = textwrap.dedent(self.META).strip()
        return meta.replace('WEBTITLE', webtitle)

    def make_webtitle(self, hostname):
        if not hostname:
            return 'Modules'
        return f'Modules — {hostname} documentation'

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )


class ModulesTableMaker:
    """Makes an overview table for python modules.
    """

    def make_table(self, modules) -> str:
        scripts = self.modules_to_scripts(modules)
        return self.run_table_printer(scripts)

    def run_table_printer(self, scripts):
        table_printer = pyoutline.ModulesTablePrinter()
        return table_printer.dumptable(scripts)

    def modules_to_scripts(self, modules):

        converter = self.module_to_script

        return list(
            map(converter, modules)
        )

    def module_to_script(self, pymod):

        name = pymod.__name__
        docs = pymod.__doc__ or ''

        return pyoutline.ScriptSketch(
            name, docs=docs, imports=None
        )
