# -*- coding: utf-8 -*-
"""Utility functions and classes.
"""

import os

__all__ = [
    'cleardocs', 'clearcache'
]


def apiobj(obj):
    obj.__module__ = 'docspy'
    return obj


def formatdoc(**kwargs):

    def _formatdoc(obj):
        obj.__doc__ = obj.__doc__.format(**kwargs)
        return obj

    return _formatdoc


def escapemd(obj):
    obj.__doc__ = obj.__doc__.replace('`__', '`&lowbar;&lowbar;')
    return obj


class DirNotFoundError(Exception):
    """Raised when a specified directory is not found.
    """


def check_srcfile(filepath):

    if not os.path.isfile(filepath):
        raise FileNotFoundError(
            f"source file not found: '{filepath}'"
        )

    return filepath


def check_srcdir(srcpath) -> str:

    srcpath = srcpath.rstrip('\\/')

    if not os.path.isdir(srcpath):
        raise DirNotFoundError(
            f"source directory does not exist: '{srcpath}'"
        )

    return srcpath


def check_docdir(docpath) -> str:

    docpath = docpath.rstrip('\\/')

    if not os.path.isdir(docpath):
        raise DirNotFoundError(
            f"documentation folder does not exist: '{docpath}'"
        )

    return docpath


@apiobj
def cleardocs(dirpath):
    """Removes HTML, CSS, JS and MD files from a specified folder.
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
        '.md', '.html', '.css', '.js'
    ]


def cleardir(dirpath):

    dirpath = check_srcdir(dirpath)

    for filename in os.listdir(dirpath):
        os.remove(
            path=os.path.join(dirpath, filename)
        )


@apiobj
@escapemd
def clearcache(rootpath=None):
    """Removes content of `__pycache__` folders in a directory tree.

    Parameters
    ----------
    rootpath : str
        Path to the root of the directory tree.

    """

    if rootpath is None:
        rootpath = os.getcwd()

    if not os.path.isdir(rootpath):
        raise ValueError(
            f"directory does not exist: '{rootpath}'"
        )

    for val in os.walk(rootpath):

        dirpath, _, _ = val

        if dirpath.endswith('__pycache__'):
            cleardir(dirpath)


def read_file(filepath) -> str:

    with open(filepath, encoding='utf-8') as file:
        return file.read()


def dump_file(filepath, content):
    with open(filepath, encoding='utf-8', mode='w') as file:
        file.write(content)
