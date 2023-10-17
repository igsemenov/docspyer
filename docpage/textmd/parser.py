# -*- coding: utf-8 -*-
"""Converts MD text to a list of MD blocks.
"""

import re
from . import blocks


def parsetext(text) -> list:
    """Converts MD text to a list of MD blocks.
    """
    parser = MDParser()
    return parser.parse(text)


class MDParser:
    """Converts MD text to a list of MD blocks.
    """

    CODEPREFIX = '```'

    def __init__(self):
        self.set_par_type_finder()
        self.set_blocks_factory()

    def set_par_type_finder(self):
        self.par_type_finder = ParTypeFinder()

    def set_blocks_factory(self):
        self.blocks_factory = BlocksFactory()

    def parse(self, text) -> list:
        """Converts MD text to a list of MD blocks.
        """

        text = self.fixcodeblocks(text)
        pars = self.fetchpars(text)

        mdblocks = list(
            map(self.convertpars, pars)
        )

        return mdblocks

    def convertpars(self, par):
        """Converts a paragraph to an MD block.
        """
        partype = self.find_par_type(par)
        return self.make_block_by_type(par, partype)

    def find_par_type(self, par):
        typefinder = self.par_type_finder.find_type
        return typefinder(par)

    def make_block_by_type(self, par, partype):
        blocksmaker = self.blocks_factory.make_block
        return blocksmaker(par, partype)

    def fixcodeblocks(self, text) -> str:
        """Formats code blocks in text as single paragraphs.
        """

        lines = text.splitlines(True)
        codepref = self.CODEPREFIX

        iscode = False
        newlines = []
        for line in lines:

            if line.startswith(codepref):
                iscode = not iscode
                newline = self.CODEPREFIX + line
            else:
                newline = self.add_codepref_to_code_lines(line, iscode)

            newlines.append(newline)

        if iscode:
            raise ValueError("text has unclosed code blocks")

        return ''.join(newlines)

    def add_codepref_to_code_lines(self, line, iscode):
        if iscode:
            return self.CODEPREFIX + line
        return line

    def fetchpars(self, text) -> list[str]:
        pars = re.split('\n\s{0,}\n', text)
        return list(
            filter(len, map(str.strip, pars))
        )


class ParTypeFinder:

    RE_HRULE = re.compile(
        blocks.MDHrule.RE_HRULE
    )

    RE_HEADNG = re.compile(
        blocks.MDHeading.RE_PREF
    )

    RE_LISTITER = re.compile(
        blocks.MDList.ITER
    )

    def __init__(self):

        self.types_map = None
        self.table_parser = None

        self.set_types_map()
        self.set_table_parser()

    def set_table_parser(self):
        self.table_parser = TableFinder()

    def set_types_map(self):

        self.types_map = {
            'hrule': self.is_hrule,
            'heading': self.is_heading,
            'list': self.is_list,
            'table': self.is_table,
            'code': self.is_code
        }

    def find_type(self, par):

        res = self.search_in_types_map(par)

        if res is not None:
            return res

        return self.say_par_otherwise()

    def search_in_types_map(self, par) -> str | None:

        for name, cheker in dict.items(self.types_map):
            if cheker(par):
                return name

        return None

    def is_hrule(self, par):
        if par.count('\n'):
            return False
        return self.match_re_hrule(par)

    def is_heading(self, par):
        if par.count('\n') > 0:
            return False
        return self.match_re_heading(par)

    def is_list(self, par):
        return self.starts_with_listiter(par)

    def is_code(self, par):
        if not par.count('\n'):
            return False
        if self.wrapped_with_code_prefix(par):
            return True
        return False

    def is_table(self, par):
        return self.table_parser.is_table(par)

    def say_par_otherwise(self):
        return 'par'

    def match_re_heading(self, text):
        return bool(
            re.match(self.RE_HEADNG, text)
        )

    def match_re_hrule(self, text):
        return bool(
            re.fullmatch(self.RE_HRULE, text)
        )

    def starts_with_listiter(self, text):
        return bool(
            re.match(self.RE_LISTITER, text)
        )

    def wrapped_with_code_prefix(self, text):
        return text.startswith('```') and text.endswith('```')


class TableFinder:
    """Checks whether a paragraph is a table.
    """

    def is_table(self, par):

        if not self.is_multiline(par):
            return False
        if not self.at_least_one_bar(par):
            return False

        lines = par.splitlines()

        if len(lines) == 1:
            return False

        if not self.equal_bars_per_line(lines):
            return False
        if not self.second_line_is_dashed(lines):
            return False

        return True

    def at_least_one_bar(self, par):
        return par.find('|') != -1

    def is_multiline(self, par):
        return bool(
            par.count('\n')
        )

    def equal_bars_per_line(self, lines):

        counts = [
            line.count('|') for line in lines
        ]

        return len(set(counts)) == 1

    def second_line_is_dashed(self, lines):
        return len(lines[1].strip('-| ')) == 0


class BlocksFactory:

    CODEPREFIX = MDParser.CODEPREFIX

    def __init__(self):
        self.set_blocks_zoo()

    def set_blocks_zoo(self):

        self.blocks_zoo = {
            'hrule': self.make_hrule,
            'heading': self.make_heading,
            'list': self.make_list,
            'table': self.make_table,
            'code': self.make_code_block,
            'par': self.make_par
        }

    def make_block(self, par, partype):
        return self.run_maker_from_blocks_zoo(par, partype)

    def run_maker_from_blocks_zoo(self, par, partype):
        return self.blocks_zoo[partype](par)

    def make_par(self, par):
        return blocks.MDPar(par)

    def make_hrule(self, par):
        return blocks.MDHrule(par)

    def make_heading(self, par):
        return blocks.MDHeading(par)

    def make_list(self, par):
        return blocks.MDList(par)

    def make_table(self, par):
        return blocks.MDTable(par)

    def make_code_block(self, par):

        lines = par.splitlines()
        lines = self.remove_codepref_from_lines(lines)

        return blocks.MDCode(
            text='\n'.join(lines)
        )

    def remove_codepref_from_lines(self, lines):
        return [
            line.removeprefix(self.CODEPREFIX) for line in lines
        ]
