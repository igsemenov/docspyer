# -*- coding: utf-8 -*-
"""Tests the maker of MD tables.
"""

import unittest
from docspyer.utils.tableasmd import maketablemd


def testrun(name):
    data = globals()['DATA_'+name]
    table = globals()['TABLE_'+name]
    assert maketablemd(data) == table.strip()


# A table with headers only.

TABLE_ONLY_HEADERS = """
Alfa | Bravo
---- | -----
"""

DATA_ONLY_HEADERS = [
    ['Alfa'], ['Bravo']
]

# A table with one short column.
# Empty columns are excluded from input data.

TABLE_ONE_COLUMN = """
| Name  |
| ----- |
| Alfa  |
| Bravo |
"""

DATA_ONE_COLUMN = [
    ['Name', 'Alfa', 'Bravo'], [], []
]

# A typical table with two short columns.
# Table length is defined by the shortest column.

TABLE_TWO_COLUMNS = """
Name  | Description
----- | -----------
Alfa  | First item 
Bravo | Second item
"""

DATA_TWO_COLUMNS = [
    ['Name', 'Alfa', 'Bravo', 'Charlie', 'Delta'],
    ['Description', 'First item', 'Second item']
]

# A table with a long item.
# Column lines are of the same length equal to the longest item.

TABLE_TWO_COLUMNS_LONG_ITEM = """
Name  | Description          
----- | ---------------------
Alfa  | First item           
Bravo | Some long description
"""

DATA_TWO_COLUMNS_LONG_ITEM = [
    ['Name', 'Alfa', 'Bravo'],
    ['Description', 'First item', 'Some long description']
]

# Using of multiline input data.
# Multiline items are unfolded when making a table.

TABLE_MULTILINE_ITEM = """
Name  | Description          
----- | ---------------------
Alfa  | First item           
Bravo | Some long description
"""

DATA_MULTILINE_ITEM = [
    ['Name', 'Alfa', 'Bravo'],
    ['Description', 'First item', 'Some \n long \n description']
]


class TestAPI(unittest.TestCase):

    def test_only_headers(self):
        testrun(name='ONLY_HEADERS')

    def test_one_column(self):
        testrun(name='ONE_COLUMN')

    def test_tow_columns(self):
        testrun(name='TWO_COLUMNS')

    def test_two_columns_long_item(self):
        testrun(name='TWO_COLUMNS_LONG_ITEM')

    def test_multiline_item(self):
        testrun(name='MULTILINE_ITEM')


if __name__ == '__main__':
    unittest.main()
