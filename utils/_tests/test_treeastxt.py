# -*- coding: utf-8 -*-
"""Test dumping trees to plain text.
"""

import unittest
from docspyer.utils.treeastxt import dumptree_txt

NO_HEADER_NO_NESTED = """
• +
  ├─ A
  └─ B
"""

WITH_HEADER_NO_NESTED = """
• O
  ├─ A
  └─ B
"""

NO_HEADER_WITH_NESTED = """
• +
  ├─ A
  │  ├─ C
  │  └─ D
  └─ B
"""


class Node:

    def __init__(self, data):
        self.data = data
        self.children = None


class TestTreePrinter(unittest.TestCase):

    def test_no_header_no_nested(self):

        root = Node('')

        root.children = [
            Node('A'), Node('B')
        ]

        assert dumptree_txt(root) == NO_HEADER_NO_NESTED.strip()

    def test_with_header_no_nested(self):

        root = Node('O')

        root.children = [
            Node('A'), Node('B')
        ]

        assert dumptree_txt(root) == WITH_HEADER_NO_NESTED.strip()

    def test_no_header_with_nested(self):

        root = Node('')

        root.children = [
            Node('A'), Node('B')
        ]

        root.children[0].children = [
            Node('C'), Node('D')
        ]

        assert dumptree_txt(root) == NO_HEADER_WITH_NESTED.strip()


if __name__ == '__main__':
    unittest.main()
