# -*- coding: utf-8 -*-
"""Operations with python scripts.
"""

import os
import itertools as itr

from . import pyparser
from . import pyreport
from ..docpage import pagemaker


__all__ = [
    'getscripts', 'Scripts'
]


def apiobj(obj):
    obj.__module__ = 'docspyer.inspect'
    return obj


@apiobj
def getscripts(dirpath):
    """Extracts python scripts from a specified folder.

    Parameters
    ----------
    dirpath : str
        Path to the folder with the scripts.

    Returns
    -------
    Scripts
        Object that holds script records.

    """

    if not os.path.isdir(dirpath):
        raise ValueError('argument is not an existing directory')

    scripts = Scripts()
    scripts.set_scripts(dirpath)

    return scripts


@apiobj
class Scripts:
    """Represents python scripts fetched from a folder.

    Attributes
    ----------
    dirpath : str
        Path to the folder with the scripts.
    scripts : dict
        Namespace of the scripts (name-to-record).

    """

    def __init__(self):
        self.dirpath = ''
        self.scripts = {}

    def listscripts(self) -> list[str]:
        """Returns names of the scripts.
        """
        return list(
            dict.keys(self.scripts)
        )

    def getscripts(self) -> list:
        """Returns records of the scripts.
        """
        return list(
            dict.values(self.scripts)
        )

    def set_dirpath(self, dirpath):

        if not os.path.isdir(dirpath):
            raise ValueError(
                f'`{dirpath}` is not an existing directory'
            )

        self.dirpath = dirpath

    def set_scripts(self, dirpath):
        self.set_dirpath(dirpath)
        records = self.get_script_records()
        self.scripts = self.make_namespace_of_scripts(records)

    def get_script_records(self) -> list:
        path = self.dirpath
        return self.call_scripts_fetcher(path)

    def call_scripts_fetcher(self, path):
        scripts_fetcher = ScriptsFetcher()
        return scripts_fetcher.getscripts(path)

    def make_namespace_of_scripts(self, scriptrecords) -> dict:

        namesgetter = self.get_names_from_records
        scriptnames = namesgetter(scriptrecords)

        mapper = self.map_names_to_records

        return mapper(
            names=scriptnames, records=scriptrecords
        )

    def get_names_from_records(self, scriptrecs):
        return [
            scriptrec.name for scriptrec in scriptrecs
        ]

    def map_names_to_records(self, names, records) -> dict:
        return dict(
            zip(names, records)
        )


class ScriptRecord:
    """Represents a python script.

    Attributes
    ----------
    name : str
        Script name.
    source : str
        Script content.

    """

    def __init__(self, name, source):
        self.name = name
        self.source = source

    def parse(self):
        return self.run_pyparser(
            source=self.source, name=self.name
        )

    def dumpdocpage(self, filepath):

        reportmaker = self.makereport

        self.run_pagemaker(
            report=reportmaker(), filepath=filepath
        )

    def dumpreport(self, filepath):

        reportmaker = self.makereport

        self.save_to_file(
            filepath, reportmaker()
        )

    def makereport(self) -> str:
        return self.run_pyreport(
            source=self.source, name=self.name
        )

    def run_pagemaker(self, report, filepath):

        filename = os.path.basename(filepath)
        webtitle, _ = os.path.splitext(filename)

        settings = pagemaker.PageParamsHTML()
        settings.webtitle = webtitle

        docpage = pagemaker.makedocpage(
            sourcemd=report, settings=settings
        )

        with open(filepath, encoding='utf-8', mode='w') as file:
            file.write(docpage)

    def run_pyparser(self, source, name):
        return pyparser.parsescript(source, name)

    def run_pyreport(self, source, name) -> str:
        return pyreport.makereport(source, name)

    def save_to_file(self, filepath, content):
        with open(filepath, encoding='utf-8', mode='w') as file:
            file.write(content)


class ScriptsFetcher:
    """Fetches python scripts from a specified folder.
    """

    def __init__(self):
        self._dirpath = None

    def getscripts(self, dirpath) -> list:

        names = self.get_script_names(dirpath)

        self._dirpath = dirpath

        sources = self.read_script_sources(names)
        records = self.make_script_records(names, sources)

        return records

    def get_script_names(self, dirpath) -> list[str]:

        files = os.listdir(dirpath)

        scripts = list(
            filter(self.is_python_script, files)
        )

        names = [
            script.removesuffix('.py') for script in scripts
        ]

        names = self.remove_private_names(names)
        return names

    def read_script_sources(self, scriptnames) -> list[str]:

        reader = self.read_script_source

        return list(
            map(reader, scriptnames)
        )

    def make_script_records(self, names, sources):

        def makerec(name, source):
            return ScriptRecord(name, source)

        return list(
            itr.starmap(makerec, zip(names, sources))
        )

    def read_script_source(self, scriptname) -> str:

        path = os.path.join(
            self._dirpath, scriptname + '.py'
        )

        with open(path, encoding='utf-8') as file:
            source = file.read()

        return source

    def is_python_script(self, filename):
        return filename.endswith('.py')

    def remove_private_names(self, names) -> list[str]:
        def is_not_private(name):
            return not name.startswith('_')
        return list(
            filter(is_not_private, names)
        )
