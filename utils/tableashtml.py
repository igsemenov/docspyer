# -*- coding: utf-8 -*-
"""Renders text data as an HTML table.
"""

import textwrap


def maketablehtml(columns, indent=4) -> str:
    """Renders lists of strings (columns) as an HTML table.

    Parameters
    ----------
    columns : Iterable[list[str]]
        Table columns as lists of strings.
    indent : int
        Number of spaces per indentation level.

    Returns
    -------
    str
        The resulting table in HTML.

    """
    table_printer = TablePrinter(indent)
    return table_printer.make_table(columns)


class TablePrinter:
    """Converts lists of strings to an HTML table.
    """

    def __init__(self, indent=2):
        self.indent = indent
        self.set_row_formatter(indent)

    def set_row_formatter(self, indent):
        self.row_formatter = RowFormatter(indent)

    def make_table(self, columns: list) -> str:

        columns = self.prepare_columns(columns)

        if not columns:
            return ''

        rows = self.convert_columns_to_rows(columns)
        rows = self.handle_rows(rows)

        return self.dump_to_table_tag(rows)

    def prepare_columns(self, columns: list) -> list:
        columns = self.clear_empties(columns)
        columns = self.unify_length(columns)
        return columns

    def clear_empties(self, columns) -> list:
        return list(
            filter(len, columns)
        )

    def unify_length(self, columns) -> list:

        minlen = min(map(len, columns))

        return [
            column[0:minlen] for column in columns
        ]

    def handle_rows(self, rows: list) -> list:
        rows = self.rows_to_html(rows)
        rows = self.format_header(rows)
        rows = self.join_and_indent(rows)
        return rows

    def rows_to_html(self, rows) -> list:

        formatter = self.row_formatter.make_row

        return list(
            map(formatter, rows)
        )

    def format_header(self, rows) -> list:
        rows[0] = rows[0].replace('<td>', '<th>')
        rows[0] = rows[0].replace('</td>', '</th>')
        return rows

    def join_and_indent(self, rows) -> list:
        return textwrap.indent(
            text='\n'.join(rows), prefix=self.indent*chr(32)
        )

    def dump_to_table_tag(self, text):
        return f'<table>\n{text}\n</table>'

    def convert_columns_to_rows(self, columns):

        def getrow(columns):
            return list(map(list.pop, columns))

        columns = [
            list(reversed(column)) for column in columns
        ]

        minlen = min(map(len, columns))

        return [
            getrow(columns) for i in range(minlen)
        ]


class RowFormatter:
    """Formats a list of strings as a table row.
    """

    def __init__(self, indent):
        self.indent = indent

    def make_row(self, strings) -> str:

        if not strings:
            return ''

        strings = self.unfold_each_string(strings)
        items = self.render_strings_as_items(strings)

        return self.assemble_items(items)

    def assemble_items(self, items) -> str:
        items = self.join_and_indent(items)
        return self.dump_to_tr_tag(items)

    def render_strings_as_items(self, strings) -> list[str]:
        return list(
            map(self.dump_to_td_tag, strings)
        )

    def unfold_each_string(self, strings):
        return list(
            map(self.text_to_line, strings)
        )

    def text_to_line(self, text) -> str:
        return ' '.join(text.split())

    def join_and_indent(self, items) -> str:
        prefix = self.indent*chr(32)
        items = '\n'.join(items)
        return textwrap.indent(items, prefix)

    def dump_to_td_tag(self, text):
        return f'<td>{text}</td>'

    def dump_to_tr_tag(self, text):
        return f'<tr>\n{text}\n</tr>'
