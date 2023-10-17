# -*- coding: utf-8 -*-
"""Creates MD documentation for a group of python modules.
"""

import os
from ..utils import contentsmd
from ..inspect import pyoutline, pydocmd
from .utils import apiobj, dump_file

__all__ = [
    'docmods'
]


@apiobj
def docmods(modules, docpath, **settings) -> None:
    """Creates MD documentation for python modules.

    Parameters
    ----------
    modules : list
        List of python modules (live objects).
    docpath : str
        Path where to place the output files.
    settings : dict
        Configuration settings (see below).

    Settings
    --------
    docsname : str = None
        Name of the index file.
        The file is omitted, if no name is given.
    hostname : str = None
        Name of the modules holder. 
        If None, the longest common name is used. 
    npstyle : bool = True
        Expects numpy style docstrings, if True.
        Otherwise, plain text format is used.
    moddocs : bool = True
        If False, modules are not documented, 
        only the index file is processed.
    modrefs : bool = True
       If True, the modules reference is added to the index file.
    clsverbs : int = 0
        Controls the verbosity of classes (0-2)
        regarding the methods headings.
    codeblocks : bool = False
        Code highlighting is activated, if True.

    """

    recorder = ModsRecorder()

    recorder.doc_modules(
        modules, docpath, **settings
    )


class ModsRecorder:
    """Makes MD documentation for a group of python modules.
    """

    def __init__(self):
        self._config = None
        self._docpath = None

    def doc_modules(self, modules, docpath, **config) -> None:

        if not modules:
            return

        self._docpath = docpath

        self.set_config(config)
        self.set_hostname(modules)

        moddocs = self.make_moddocs(modules)
        outline = self.make_outline(moddocs, modules)

        self.dump_files(outline, moddocs)

    def set_config(self, config) -> dict:
        self._config = self.get_default_config()
        self._config = self.update_config(config)

    def get_default_config(self) -> dict:
        return {
            'docsname': None,
            'hostname': None,
            'npstyle': True,
            'moddocs': True,
            'modrefs': True,
            'clsverbs': 0,
            'codeblocks': False
        }

    def update_config(self, config) -> dict:
        return self._config | config

    def set_hostname(self, modules):
        hostname = self.get_hostname(modules)
        self.update_hostname(hostname)

    def get_hostname(self, modules):
        return self.get_common_name(modules)

    def update_hostname(self, hostname):
        self._config['hostname'] = self._config['hostname'] or hostname

    def make_moddocs(self, modules) -> dict:
        return ModsDocser().get_sources(modules, self._config)

    def make_outline(self, sources, modules) -> str:
        return OutlineMaker().make_outline(sources, modules, self._config)

    def dump_files(self, outline, moddocs):

        dumper = self.dump_file

        self.dump_outline(outline, dumper)
        self.dump_moddocs(moddocs, dumper)

    def dump_outline(self, outline, filedumper):

        if not self._config['docsname']:
            return

        filedumper(
            name=self._config['docsname'], content=outline
        )

    def dump_moddocs(self, sources, filedumper):

        if not self._config['moddocs']:
            return

        for name, content in sources.items():
            filedumper(name, content)

    def dump_file(self, name, content):

        if not name:
            return
        if not content:
            return

        filepath = os.path.join(
            self._docpath, name + '.md'
        )

        dump_file(filepath, content)

    def get_common_name(self, pymods):
        names = [mod.__name__ for mod in pymods]
        prefix = os.path.commonprefix(names)
        hostname, _, _ = prefix.partition('.')
        return hostname


class ModsDocser:
    """Generates MD source files for modules.
    """

    def __init__(self):
        self._config = None

    def get_sources(self, modules, config) -> dict:

        self._config = config.copy()

        docs = list(
            map(self.module_to_md, modules)
        )

        names = [
            mod.__name__ for mod in modules
        ]

        return dict(zip(names, docs))

    def module_to_md(self, pymod) -> str:
        meta = self.specify_module_meta()
        docs = self.run_pydocmd(pymod, meta)
        return docs

    def run_pydocmd(self, pymod, meta):

        config = {
            'meta': meta,
            'npstyle': self._config['npstyle'],
            'clsverbs': self._config['clsverbs']
        }

        return pydocmd.modtomd(pymod, **config)

    def specify_module_meta(self):
        return {
            "webtitle": self.make_module_webtitle(),
            "codeblocks": self._config['codeblocks']
        }

    def make_module_webtitle(self):

        hostname = self._config['hostname']

        if not hostname:
            return 'Modules'
        return f'Modules — {hostname} documentation'


class OutlineMaker:
    """Creates the index file (outline).
    """

    def __init__(self):
        self._config = None

    def make_outline(self, moddocs, modules, config):

        self._config = config.copy()

        meta = self.get_meta()
        table = self.make_table(modules)
        modrefs = self.make_modrefs(moddocs)

        return self.assemble(meta, table, modrefs)

    def make_table(self, modules):
        table = self.run_tablemaker(modules)
        title = self.set_table_heading()
        return self.assemble(title, table)

    def make_modrefs(self, moddocs):
        refs = self.run_refsmaker(moddocs)
        title = self.set_refs_heading()
        return self.assemble(title, refs)

    def run_tablemaker(self, modules) -> str:
        return TableMaker().make_table(modules)

    def run_refsmaker(self, moddocs) -> str:

        if not self._config['modrefs']:
            return ''

        refs = self.make_multitoc(moddocs)
        refs = self.add_css_class(refs)

        return refs

    def make_multitoc(self, sources):
        return contentsmd.makemultitoc(sources, level=3)

    def add_css_class(self, refs):
        return refs.replace(
            '<p>\n<ul>', '<p>\n<ul class="ref-list" id="mod-refs">'
        )

    def set_table_heading(self) -> str:
        if self._config['modrefs']:
            return '## Annotations'
        return '<i>Annotations</i>'

    def set_refs_heading(self):
        if self._config['modrefs']:
            return '## Reference'
        return ''

    def get_meta(self):

        hostname = self._config['hostname']

        web = self.make_webtitle(hostname)
        doc = self.make_doctitle(hostname)

        web = f'"webtitle": "{web}"'
        doc = f'"doctitle": "{doc}"'

        meta = f'<!--\n{{\n  {web},\n  {doc}\n}}\n-->'
        return meta

    def make_webtitle(self, hostname):
        if not hostname:
            return 'Modules'
        return f'Modules — {hostname} documentation'

    def make_doctitle(self, hostname):
        if not hostname:
            return 'Modules'
        return f'{hostname} — Modules'

    def assemble(self, *parts):
        return '\n\n'.join(
            filter(len, parts)
        )


class TableMaker:
    """Makes an overview table for python modules.
    """

    def make_table(self, modules) -> str:
        scripts = self.modules_to_scripts(modules)
        return self.run_modstable_maker(scripts)

    def run_modstable_maker(self, scripts):
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
