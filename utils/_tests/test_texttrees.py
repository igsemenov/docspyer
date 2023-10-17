# -*- coding: utf-8 -*-
"""Test the converter of text lists to trees.
"""

import unittest
from docspyer.utils import treeastxt
from docspyer.utils.texttrees import maketree, TextSplitter

dumptree = treeastxt.dumptree_txt

# A plain text list.

PLAIN_LIST = """
- A
- B
"""

TREE_PLAIN_LIST = """
• +
  ├─ A
  └─ B
"""

# A text list with nested items.

LIST_WITH_NESTED = """
- A
  - C
- B
"""

TREE_LIST_WITH_NESTED = """
• +
  ├─ A
  │  └─ C
  └─ B
"""

# A text list with a multiline item.

LIST_MULTILINE_ITEM = """
- Alfa
- Bravo
Charlie
Delta
"""

MULTILINE_ITEM = """
Bravo
Charlie
Delta
"""


class TestTreeMaker(unittest.TestCase):

    def test_plain_list(self):
        root = maketree(PLAIN_LIST)
        assert dumptree(root) == TREE_PLAIN_LIST.strip()

    def test_list_with_nested(self):
        root = maketree(LIST_WITH_NESTED)
        assert dumptree(root) == TREE_LIST_WITH_NESTED.strip()

    def test_list_with_multiline_item(self):
        root = maketree(LIST_MULTILINE_ITEM)
        assert root.children[1].data == MULTILINE_ITEM.strip()


class TestTextSplitter(unittest.TestCase):

    def test_fetch_header_no_items(self):
        assert TextSplitter().fetch_header('A') == 'A'

    def test_fetch_header_with_items(self):
        assert TextSplitter().fetch_header('A\n- B') == 'A'
        assert TextSplitter().fetch_header('A\n - B') == 'A'

    def test_fetch_items_no_nested(self):
        assert TextSplitter().fetch_items('A\n- B\n- C') == ['B', 'C']

    def test_fetch_items_with_nested(self):
        assert TextSplitter().fetch_items('A\n- B\n - C') == ['B\n - C']


if __name__ == '__main__':
    unittest.main()
