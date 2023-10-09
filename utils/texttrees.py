# -*- coding: utf-8 -*-
"""Converts text lists into trees.
"""

import re
import textwrap


def maketree(text_with_list):
    """Converts a text list into a tree and returns the root.
    """
    tree_maker = TreeMaker()
    return tree_maker.make_tree(text_with_list)


class TreeMaker:
    """Makes a tree by splitting text into items.
    """

    def __init__(self):
        self.set_text_splitter()

    def set_text_splitter(self):
        self.text_splitter = TextSplitter()

    def make_tree(self, text_with_list):
        root = TreeNode(text_with_list)
        self.walk_to_make_nodes(root)
        return root

    def walk_to_make_nodes(self, node):

        self.set_node(node)

        if node.children is None:
            return

        for child in node.children:
            self.walk_to_make_nodes(child)

    def set_node(self, node):

        header, items = self.get_header_and_items(node)

        self.header_to_node_data(node, header)

        if not items:
            return

        self.items_to_children_data(node, items)

    def get_header_and_items(self, node):
        splitter = self.text_splitter
        header, items = splitter.split_text(node.data)
        return header, items

    def header_to_node_data(self, node, header):
        node.data = header

    def items_to_children_data(self, node, items):
        node.children = list(
            map(TreeNode, items)
        )


class TextSplitter:
    """Splits text into a header and a list of items.
    """

    re_item_noindent = '^- {1,}'
    re_item_indented = '^ {0,}- '

    def split_text(self, sourcetext):

        text = sourcetext.strip().rstrip('-')

        if not text:
            return None

        header = self.fetch_header(text)
        items = self.fetch_items(text)

        return header, items

    def fetch_header(self, text) -> str:

        first_item_start = self.find_first_item(text)

        if first_item_start is None:
            header_end = len(text)
        else:
            header_end = first_item_start

        header = text[0:header_end]

        return header.strip()

    def fetch_items(self, text) -> list[str]:

        first_item_start = self.find_first_item(text)

        if first_item_start is None:
            return []

        text_with_items = text[
            first_item_start:len(text)
        ]

        text_to_split = self.dedent_items(text_with_items)

        items = re.split(
            self.re_item_noindent, text_to_split, flags=re.MULTILINE
        )

        items = map(str.strip, items)

        return list(
            filter(len, items)
        )

    def find_first_item(self, text) -> int | None:

        first_item = re.search(
            self.re_item_indented, text, flags=re.MULTILINE
        )

        if first_item is None:
            return None

        return first_item.start()

    def dedent_items(self, text) -> str:
        return textwrap.dedent(text)


class TreeNode:
    """Node of the resulting trees.

    Attributes
    ----------
    data : str
        Text data fetched from the list.
    children : list[TreeNode] | None
        Children nodes.

    """

    def __init__(self, data):
        self.data = data
        self.children = None
