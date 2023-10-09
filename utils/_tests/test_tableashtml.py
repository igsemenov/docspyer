# -*- coding: utf-8 -*-
"""Tests the maker of HTML tables.
"""

import unittest
from docspyer.utils.tableashtml import maketablehtml


def testrun(name):
    data = globals()['DATA_'+name]
    table = globals()['TABLE_'+name]
    assert maketablehtml(data) == table.strip()


# Headers only.

TABLE_ONLY_HEADERS = """
<table>
    <tr>
        <th>Alfa</th>
        <th>Bravo</th>
    </tr>
</table>
"""

DATA_ONLY_HEADERS = [
    ['Alfa'], ['Bravo']
]

# One short column.
# Empty columns are excluded from input data.

TABLE_ONE_COLUMN = """
<table>
    <tr>
        <th>Name</th>
    </tr>
    <tr>
        <td>Alfa</td>
    </tr>
</table>
"""

DATA_ONE_COLUMN = [
    ['Name', 'Alfa'], [], []
]

# Table with two short columns.
# Table length is defined by the shortest column.

TABLE_TWO_COLUMNS = """
<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Alfa</td>
        <td>Some info about Alfa</td>
    </tr>
</table>
"""

DATA_TWO_COLUMNS = [
    ['Name', 'Alfa', 'Bravo', 'Delta'],
    ['Description', 'Some info about Alfa']
]

# Multiline items in input data.
# Multiline items are unfolded when making a table.

TABLE_MULTILINE_ITEM = """
<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Alfa</td>
        <td>Some info about Alfa</td>
    </tr>
</table>
"""

DATA_MULTILINE_ITEM = [
    ['Name', 'Alfa'],
    ['Description', 'Some \n info \n about \n Alfa']
]


class TestAPI(unittest.TestCase):

    def test_only_headers(self):
        testrun('ONLY_HEADERS')

    def test_one_column(self):
        testrun('ONE_COLUMN')

    def test_two_columns(self):
        testrun('TWO_COLUMNS')

    def test_multiline_textdata(self):
        testrun('MULTILINE_ITEM')


if __name__ == '__main__':
    unittest.main()
