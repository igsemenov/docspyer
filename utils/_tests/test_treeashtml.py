# -*- coding: utf-8 -*-
"""Test dumping trees to HTML lists.
"""

import unittest
from docspyer.utils import treeashtml

dumptree = treeashtml.dumptree_html

NO_HEADER_NO_NESTED = """
<p>
<ul>
    <li>A</li>
    <li>B</li>
</ul>
</p>
"""

NO_HEADER_WITH_NESTED = """
<p>
<ul>
    <li>A
        <ul>
            <li>X</li>
            <li>Y</li>
        </ul>
    </li>
    <li>B</li>
</ul>
</p>
"""

WITH_HEADER_NO_NESTED = """
<p>Header
<ul>
    <li>A</li>
    <li>B</li>
</ul>
</p>
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

        assert dumptree(root) == NO_HEADER_NO_NESTED.strip()

    def test_no_header_with_nested(self):

        root = Node('')

        root.children = [
            Node('A'), Node('B')
        ]

        root.children[0].children = [
            Node('X'), Node('Y')
        ]

        assert dumptree(root) == NO_HEADER_WITH_NESTED.strip()

    def test_with_header_no_nested(self):

        root = Node('Header')

        root.children = [
            Node('A'), Node('B')
        ]

        assert dumptree(root) == WITH_HEADER_NO_NESTED.strip()


if __name__ == '__main__':
    unittest.main()
