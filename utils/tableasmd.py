# -*- coding: utf-8 -*-
"""Renders text data as an MD table.
"""


def maketablemd(columns) -> str:
    """Renders lists of strings (columns) as an MD table.

    Parameters
    ----------
    columns : Iterable[list[str]]
        Table columns as lists of strings.

    Returns
    -------
    str
        The resulting MD table.

    """
    table_printer = TablePrinter()
    return table_printer.make_table(columns)


class TablePrinter:
    """Converts lists of strings to an MD table.
    """

    def __init__(self):
        self.set_column_formatter()

    def set_column_formatter(self):
        self.column_formatter = ColumnFormatter()

    def make_table(self, columns) -> str:

        columns = self.prepare_columns(columns)

        if not columns:
            return ''

        columns = self.format_columns_as_strings(columns)
        table = self.join_columns_line_by_line(columns)

        return table

    def prepare_columns(self, columns) -> list:
        columns = self.exclude_empties(columns)
        columns = self.unify_length(columns)
        return columns

    def exclude_empties(self, columns) -> list:
        return list(
            filter(len, columns)
        )

    def unify_length(self, columns) -> list:

        minlen = min(map(len, columns))

        return [
            column[0:minlen] for column in columns
        ]

    def format_columns_as_strings(self, columns):

        formatter = self.column_formatter.make_column

        return list(
            map(formatter, columns)
        )

    def join_columns_line_by_line(self, columns_as_strings) -> str:

        columns = list(
            map(str.splitlines, columns_as_strings)
        )

        items = zip(*columns)

        joiner = self.join_items_across_line

        return '\n'.join(
            map(joiner, items)
        )

    def join_items_across_line(self, items) -> str:
        if len(items) == 1:
            return '| ' + items[0] + ' |'
        return ' | '.join(items)


class ColumnFormatter:
    """Formats a list of strings as a table column.
    """

    def make_column(self, strings) -> str:

        if not strings:
            return ''

        strings = self.unfold_each_string(strings)
        strings = self.unify_length_of_strings(strings)
        strings = self.underline_first_item(strings)

        column = self.join_strings_to_column(strings)

        return column

    def join_strings_to_column(self, strings):
        return '\n'.join(strings)

    def unfold_each_string(self, strings):
        return list(
            map(self.text_to_line, strings)
        )

    def unify_length_of_strings(self, strings):

        maxlen = max(map(len, strings))

        return [
            string.ljust(maxlen) for string in strings
        ]

    def underline_first_item(self, strings):
        dashed_line = '-'*len(strings[0])
        strings.insert(1, dashed_line)
        return strings

    def text_to_line(self, text) -> str:
        return ' '.join(text.split())
