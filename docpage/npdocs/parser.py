# -*- coding: utf-8 -*-
"""Parser of numpy style docstrings.
"""

import re
import textwrap
from . import blocks


def parsedoc(docstr) -> list:
    """Converts a numpy style docstring to a list of structural blocks.

    Parameters
    ----------
    docstr : str
        Docstring to be converted.

    Returns
    -------
    list
        Structural blocks of the docstring.

    """
    parser = DocParser()
    return parser.parsedoc(docstr)


class DocParser:

    def __init__(self):
        self.parreader = None
        self.set_parreader()

    def set_parreader(self):
        self.parreader = ParReader()

    def parsedoc(self, docstr):
        pars = self.fetchpars(docstr)
        return self.readpars(pars)

    def fetchpars(self, text) -> list[str]:
        return fetchpars(text)

    def readpars(self, pars) -> list:
        return list(
            map(self.parreader.par_to_block, pars)
        )


class ParReader:
    """Converts a paragraph into a block.
    """

    sections = (
        'Notes',
        'Methods',
        'Examples',
        'See Also',
        'Notations'
    )

    varlists = (
        'Parameters',
        'Attributes',
        'Properties',
        'Settings',
        'Returns',
        'Raises',
        'Keys'
    )

    re_varlists = "(" + "|".join(varlists) + ")"
    re_sections = "(" + "|".join(sections) + ")"

    re_varlist_header = re.compile(
        re_varlists + r"\n-{3,}(\n|$)"
    )

    re_section_header = re.compile(
        re_sections + r"\n-{3,}(\n|$)"
    )

    def __init__(self):
        self.factories = None
        self.set_factories()

    def set_factories(self):

        self.factories = {
            'section': SectionFactory(),
            'varlist': VarlistFactory(),
            'textdata': TextdataFactory()
        }

    def par_to_block(self, par):
        partype = self.find_partype(par)
        factory = self.take_factory_by_type(partype)
        return self.make_block_by_factory(par, factory)

    def make_block_by_factory(self, par, factory):
        return factory.make_block(par)

    def take_factory_by_type(self, partype):
        return self.factories[partype]

    def find_partype(self, par):
        if self.say_if_section(par):
            return 'section'
        if self.say_if_varlist(par):
            return 'varlist'
        return self.say_textdata_otherwise()

    def say_if_section(self, par):
        if re.match(self.re_section_header, par):
            return True
        return False

    def say_if_varlist(self, par):
        if re.match(self.re_varlist_header, par):
            return True
        return False

    def say_textdata_otherwise(self):
        return 'textdata'


class TextdataFactory:

    def make_block(self, par):
        return blocks.Textdata(par)


class SectionFactory:
    """Creates a section as a block.
    """

    re_header_fringe = '\n-{1,}'

    def make_block(self, par):
        header = self.fetch_header(par)
        body = self.fetch_body(par)
        return self.create_block(header, body)

    def fetch_header(self, par) -> str:
        return re.split(self.re_header_fringe, par)[0]

    def fetch_body(self, par) -> str:
        return re.split(self.re_header_fringe, par)[1]

    def create_block(self, header, body):
        return blocks.Section(
            heading=header, content=body.strip()
        )


class VarlistFactory:
    """Creates a variable list as a block.
    """

    re_header_fringe = '\n-{1,}'

    def __init__(self):
        self.set_varreader()

    def set_varreader(self):
        self.varreader = VarReader()

    def make_block(self, par):
        header = self.fetch_header(par)
        body = self.fetch_body(par)
        varrecs = self.read_vars_from_body(body)
        return self.create_block(header, varrecs)

    def fetch_header(self, par) -> str:
        return re.split(self.re_header_fringe, par)[0]

    def fetch_body(self, par) -> str:
        return re.split(self.re_header_fringe, par)[1]

    def read_vars_from_body(self, body) -> list:

        if body.strip() == '':
            return []

        items = getattr(self, 'fetch_list_items')(body)

        recordsmaker = self.make_varrecords

        vardefs_fetcher = self.fetch_vardefs_from_items
        vardocs_fetcher = self.fetch_vardocs_from_items

        return recordsmaker(
            vardefs=vardefs_fetcher(items),
            vardocs=vardocs_fetcher(items)
        )

    def create_block(self, heading, variables):
        return blocks.Varlist(heading, variables)

    def make_varrecords(self, vardefs, vardocs):

        maker = self.varreader.make_record

        return [
            maker(*args) for args in zip(vardefs, vardocs)
        ]

    def fetch_list_items(self, listbody) -> list[str]:
        newbody = self.format_items_as_pars(listbody)
        return self.fetch_items_as_pars(newbody)

    def format_items_as_pars(self, listbody):
        return self.isolate_vardefs(listbody)

    def isolate_vardefs(self, listbody) -> str:

        def isolate_vardef(line):
            if not line.startswith(' '):
                return '\n' + line + '\n'
            return line

        bodylines = str.splitlines(listbody)

        newbody = '\n'.join(
            map(isolate_vardef, bodylines)
        )

        return newbody

    def fetch_items_as_pars(self, listbody):

        items = fetchpars(listbody)

        return list(
            filter(len, items)
        )

    def fetch_vardefs_from_items(self, items) -> list:

        selector = self.is_vardef

        return [
            item for item in items if selector(item)
        ]

    def fetch_vardocs_from_items(self, items) -> list:

        selector = self.is_vardef

        return [
            item for item in items if not selector(item)
        ]

    def is_vardef(self, item):

        is_line = item.count('\n') == 0
        not_indented = not item.startswith(' ')

        return not_indented and is_line


class VarReader:
    """Makes a variable record from a variable definition and docstring.
    """

    def make_record(self, vardef, vardoc):

        varname, vartype = self.parse_vardef(vardef)
        vardoc = self.dedent_vardoc(vardoc)

        return self.create_record(varname, vartype, vardoc)

    def create_record(self, varname, vartype, vardoc):
        return blocks.VarRecord(varname, vartype, vardoc)

    def parse_vardef(self, vardef):
        varname = self.fetch_varname(vardef)
        vartype = self.fetch_vartype(vardef)
        return varname, vartype

    def fetch_varname(self, vardef) -> str:
        if ':' in vardef:
            return vardef.split(':')[0].strip()
        return vardef.strip()

    def fetch_vartype(self, vardef) -> str:
        if ':' in vardef:
            return vardef.split(':')[1].strip()
        return ''

    def dedent_vardoc(self, vardoc) -> str:
        return textwrap.dedent(vardoc)


def fetchpars(text):

    pars = [
        par.strip('\n') for par in re.split('\n\s{0,}\n', text)
    ]

    return list(
        filter(len, pars)
    )
