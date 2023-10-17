# -*- coding: utf-8 -*-
"""Utility functions and classes.
"""

import os

__all__ = [
    'cleardocs'
]


def apiobj(obj):
    obj.__module__ = 'docspyer'
    return obj


def formatdoc(**kwargs):

    def _formatdoc(obj):
        obj.__doc__ = obj.__doc__.format(**kwargs)
        return obj

    return _formatdoc


def escapemd(obj):
    obj.__doc__ = obj.__doc__.replace('`__', '`&lowbar;&lowbar;')
    return obj


def check_srcfile(filepath):

    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"source file not found: '{filepath}'"
        )

    return filepath


def check_srcdir(srcpath) -> str:

    srcpath = srcpath.rstrip('\\/')

    if not os.path.isdir(srcpath):
        raise DirNotFound(
            f"source directory does not exist: '{srcpath}'"
        )

    return srcpath


def check_docdir(docpath) -> str:

    docpath = docpath.rstrip('\\/')

    if not os.path.isdir(docpath):
        raise DirNotFound(
            f"documentation folder does not exist: '{docpath}'"
        )

    return docpath


@apiobj
def cleardocs(dirpath) -> None:
    """Removes HTML, CSS, JS files from a specified folder.
    """

    dirpath = check_srcdir(dirpath)
    extensions = set_docs_extensions()

    def is_to_clean(filename):
        _, ext = os.path.splitext(filename)
        return ext in extensions

    filenames = list(
        filter(is_to_clean, os.listdir(dirpath))
    )

    paths = [
        os.path.join(dirpath, name) for name in filenames
    ]

    for path in paths:
        os.remove(path)


def set_docs_extensions() -> list[str]:
    return [
        '.html', '.css', '.js'
    ]


def cleardir(dirpath):

    dirpath = check_srcdir(dirpath)

    for filename in os.listdir(dirpath):
        os.remove(
            path=os.path.join(dirpath, filename)
        )


@apiobj
@escapemd
def clearcache(dirpath) -> None:
    """Removes content of `__pycache__` folders in a directory tree.

    Parameters
    ----------
    dirpath : str
        Path to the root of the directory tree.

    """

    if dirpath == '':
        raise ValueError(
            "an empty path is not allowed"
        )

    if not os.path.isdir(dirpath):
        raise ValueError(
            f"directory does not exist: '{dirpath}'"
        )

    for val in os.walk(dirpath):

        folderpath, _, _ = val

        if folderpath.endswith('__pycache__'):
            cleardir(folderpath)


def read_file(filepath) -> str:
    with open(filepath, encoding='utf-8') as file:
        return file.read()


def read_file_or_str(arg) -> str:
    if os.path.isfile(arg):
        return read_file(arg)
    return arg


def dump_file(filepath, content):
    with open(filepath, encoding='utf-8', mode='w') as file:
        file.write(content)


class DirNotFound(Exception):
    """Raised when a specified directory is not found.
    """


class FileFinder:
    """Searches for a file in specified directories.
    """

    def __init__(self, *srcdirs):
        self.srcdirs = list(srcdirs)

    def set_srcdirs(self, *srcdirs):
        self.srcdirs = list(srcdirs)

    def findfile(self, filename) -> str | None:
        """Returns the path to the file or None.
        """
        path = self.search_in_srcdirs(filename)
        return path

    def search_in_srcdirs(self, filename):
        for path in self.srcdirs:
            res = self.search_in_dir(filename, path)
            if res is not None:
                return res
        return None

    def search_in_dir(self, filename, dirpath):
        for name in os.listdir(dirpath):
            if name == filename:
                return os.path.join(dirpath, filename)
        return None


class PyName:
    """Long name of a python object.
    """

    def __init__(self):
        self._module = None
        self._class = None
        self._name = None

    def fromstr(self, fullname):
        self._module = self.fetch_module(fullname)
        self._class = self.fetch_class(fullname)
        self._name = self.fetch_name(fullname)
        return self

    def render(self):

        fullname = self.dump()

        if self._name:
            return fullname + '()'
        return fullname

    def dump(self):

        items = [
            self._module, self._class, self._name
        ]

        return '.'.join(
            filter(len, items)
        )

    def getmodule(self):
        return self._module

    def getclass(self):
        return self._class

    def getname(self):
        return self._name

    def fetch_class(self, fullname) -> str:

        classes = list(
            filter(self.isclass, fullname.split('.'))
        )

        if not classes:
            return ''
        return classes.pop()

    def fetch_module(self, fullname):

        header, *_ = fullname.rpartition('.')

        return '.'.join(
            filter(self.ismodule, header.split('.'))
        )

    def fetch_name(self, fullname):

        *_, name = fullname.rpartition('.')

        if self.isname(name):
            return name
        return ''

    def isclass(self, value):
        if value.islower():
            return False
        if value.isupper():
            return False
        return True

    def ismodule(self, value):
        return not self.isclass(value)

    def isname(self, value):
        return not self.isclass(value)

    def get_from_host(self, hostmod):
        self.check_host(hostmod)
        return self.fetch_object(hostmod)

    def check_host(self, hostmod):

        hosttype = type(hostmod).__name__

        if hosttype != 'module':
            raise ValueError(
                f"module expected, '{hosttype}' given"
            )

        objname = self.dump()
        hostname = hostmod.__name__

        if objname.startswith(hostname + '.'):
            return

        raise ValueError(
            f"'{hostname}' is not a host module of '{objname}'"
        )

    def fetch_object(self, hostmod):

        objname = self.dump()

        objname = objname.removeprefix(hostmod.__name__)
        objname = objname.lstrip('.')

        members = objname.split('.')

        val = hostmod
        for name in members:
            val = getattr(val, name)

        return val
