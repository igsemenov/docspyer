# -*- coding: utf-8 -*-
"""Custom formatter for documentation source files.
"""

import string
import textwrap
from . import utils
from .utils import FileFinder

__all__ = [
    'DocFormat'
]


@utils.apiobj
class DocFormat:
    """Custom formatter of source files.
    """

    def __init__(self):
        self.converter = None
        self.formatter = None

    def setconfig(self, srcdirs, hostmod):
        """Sets up the formatter.

        Parameters
        ----------
        srcdirs : list[str]
            Folders to search for source files.
        hostmod : module
            Module used to run inline calls.

        """
        self.set_str_formatter()
        self.set_key_converter(srcdirs, hostmod)

    def set_key_converter(self, srcdirs, hostmod):
        self.converter = KeysConverter().set_config(srcdirs, hostmod)

    def set_str_formatter(self):
        self.formatter = StrFormatter()

    def formatdoc(self, srcpath, dstpath):
        text = self.read_doc(srcpath)
        newtext = self.format_doc(text)
        self.dump_doc(dstpath, newtext)

    def format_doc(self, text):

        formatter = self.formatter

        return formatter.format(
            text, converter=self.converter.convertkey
        )

    def read_doc(self, filepath):
        return utils.read_file(filepath)

    def dump_doc(self, filepath, content):
        utils.dump_file(filepath, content)


class StrFormatter(string.Formatter):
    """Custom string formatter.

    - Customizes `string.Formatter`.
    - Runs `KeysConverter` to get replacements.

    """

    def get_value(self, key, args, kwargs):

        if isinstance(key, int):
            return key

        converter = kwargs.get('converter')

        if converter is None:
            return key

        key = key.strip('*')
        return converter(key)


class KeysConverter:
    """Converts format keys to replacements.
    """

    def __init__(self):
        self.inserter = None
        self.linker = None
        self.runner = None

    def set_config(self, srcdirs, hostmod):
        self.set_keys(srcdirs, hostmod)
        return self

    def set_keys(self, srcdirs, hostmod):
        self.inserter = Inserter().set_config(srcdirs)
        self.linker = Linker().set_config(srcdirs)
        self.runner = Runner().set_config(hostmod)

    def convertkey(self, key):
        keytype = self.get_key_type(key)
        converter = self.getconverter(keytype)
        return self.runconverter(converter, key)

    def runconverter(self, obj, key):
        if obj is None:
            return key
        return obj.convert(key)

    def getconverter(self, name):
        if not name:
            return None
        return getattr(self, name)

    def get_key_type(self, key):
        if self.is_inserter(key):
            return 'inserter'
        if self.is_linker(key):
            return 'linker'
        if self.is_runner(key):
            return 'runner'
        return None

    def is_inserter(self, key):
        if key.endswith('-py'):
            return True
        if key.endswith('-md'):
            return True
        return False

    def is_linker(self, key):
        return key.startswith('#')

    def is_runner(self, key):

        if key.endswith('()'):
            return True

        *_, suffix = key.rpartition('-')

        if suffix.isupper():
            return True

        return False


class BaseKey:
    """Base class for format keys.
    """

    def __init__(self):
        self.file_finder = None

    def set_config(self, srcdirs):
        self.set_file_finder(srcdirs)
        return self

    def set_file_finder(self, srcdirs):
        self.file_finder = FileFinder(*srcdirs)

    def get_source(self, filename, key) -> str:

        filepath = self.find_source_file(filename)

        if filepath:
            return utils.read_file(filepath)

        raise SourceNotFound(
            f"cannont find source '{filename}' for the key '{key}'"
        )

    def find_source_file(self, filename):
        finder = self.file_finder
        return finder.findfile(filename)


class Inserter(BaseKey):
    """Key to insert content of a source file.
    """

    def convert(self, key):
        value = self.get_content(key)
        return value

    def get_content(self, key):
        filename = self.key_to_filename(key)
        return self.get_source(filename, key)

    def key_to_filename(self, key):
        if key.endswith('-py'):
            return key.replace('-py', '.py')
        if key.endswith('-md'):
            return key.replace('-md', '.md')
        raise ValueError(
            f"key with an undefined source extension: '{key}'"
        )


class Linker(BaseKey):
    """Link to an object in the API reference.
    """

    def __init__(self):
        super().__init__()

        self._key = None
        self._pyname = None
        self._docname = None
        self._objname = None

    def convert(self, key):
        self.set_names(key)
        nameid = self.find_object()
        return self.render_link(nameid)

    def set_names(self, key):

        pyname = self.key_to_pyname(key)

        self._key = key
        self._pyname = pyname
        self._docname = self.pyname_to_docname(pyname)
        self._objname = self.pyname_to_objname(pyname)

    def key_to_pyname(self, key):
        name = key.replace('-', '.').lstrip('#')
        return utils.PyName().fromstr(name)

    def pyname_to_docname(self, pyname):
        return pyname.getmodule() + '.md'

    def pyname_to_objname(self, pyname):
        return pyname.render()

    def find_object(self):

        source = self.get_module_md()
        heading = self.find_heading(source)

        if not heading:
            raise ObjectNotFound(
                f"cannot find '{self._objname}' in '{self._docname}'"
            )

        return self.heading_to_id(heading)

    def get_module_md(self):
        return self.get_source(
            filename=self._docname, key=self._key
        )

    def find_heading(self, source):

        heading = PyNameFinder().findname(
            source, self._pyname
        )

        if heading:
            return heading
        return None

    def heading_to_id(self, heading):
        return heading.casefold().rstrip('()')

    def render_link(self, nameid):
        path = self._docname + '#' + nameid
        return f'[{self._objname}]({path})'


class Runner(BaseKey):
    """Key to insert the result of an inline call. 
    """

    def __init__(self):
        self.hostmod = None

    def set_config(self, hostmod):
        self.set_hostmod(hostmod)
        return self

    def set_hostmod(self, hostmod):
        self.hostmod = hostmod

    def convert(self, key):

        if not self.hostmod:
            return key

        pyname = self.key_to_pyname(key)
        obj = self.pyname_to_obj(pyname)

        output = self.run_object(obj)
        return textwrap.dedent(output)

    def pyname_to_obj(self, pyname):
        return pyname.get_from_host(self.hostmod)

    def run_object(self, obj):
        if not callable(obj):
            return str(obj)
        return obj()

    def key_to_pyname(self, key):
        name = key.rstrip('()').replace('-', '.')
        return utils.PyName().fromstr(name)


class PyNameFinder:
    """Searches for a python object in the module documentation.
    """

    def findname(self, source, pyname):
        """Returns the object heading or None.
        """

        prolog = self.split_at_definition(source, pyname)

        if not prolog:
            return None

        return self.get_heading_before_def(prolog)

    def split_at_definition(self, source, pyname):
        defstr = self.pyname_to_def(pyname)
        prolog = self.search_for_def(source, defstr)
        return prolog

    def get_heading_before_def(self, prolog):

        _, sep, header = prolog.rpartition('# ')

        if not sep:
            return None

        heading, *_ = header.partition('\n')
        return heading.strip()

    def pyname_to_def(self, pyname):

        clsname = pyname.getclass()

        if clsname:
            return self.def_with_class(pyname)
        return self.def_no_class(pyname)

    def def_with_class(self, pyname):

        name = pyname.getname()
        clsname = pyname.getclass()
        modname = pyname.getmodule()

        if not name:
            return f'{modname}.<b>{clsname}</b>'
        return f'{clsname}.<b>{name}</b>'

    def def_no_class(self, pyname):
        name = pyname.getname()
        modname = pyname.getmodule()
        return f'{modname}.<b>{name}</b>'

    def search_for_def(self, source, defstr):

        prolog, sep, _ = source.partition(defstr)

        if not sep:
            raise ObjectNotFound(
                f"object definition not found: '{defstr}'"
            )

        return prolog


class SourceNotFound(Exception):
    """Raised when the key related source file is not found.
    """


class ObjectNotFound(Exception):
    """Raised when the object is not found in the module documentation.
    """
