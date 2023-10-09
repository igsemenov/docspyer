# -*- coding: utf-8 -*-
"""Test inclusion of subtrees into trees.
"""

import unittest
from docspyer.utils import deeptrees
from docspyer.utils import treeastxt

Node = deeptrees.TreeNode
dumptree = treeastxt.dumptree_txt

PRIMARY_TREE = """
• A
  ├─ B
  └─ C
"""

SUBTREE = """
• B
  ├─ D
  └─ E
"""

FINAL_TREE = """
• A
  ├─ B
  │  ├─ D
  │  └─ E
  └─ C
"""


def make_primary_tree() -> Node:

    root = Node('A')
    root.children = [Node('B'), Node('C')]

    return root


def make_subtree() -> Node:

    subroot = Node('B')
    subroot.children = [Node('D'), Node('E')]

    return subroot


class TestBasicScenario(unittest.TestCase):

    def test_basic_scenario(self):

        root = make_primary_tree()
        subroot = make_subtree()

        assert dumptree(root) == PRIMARY_TREE.strip()
        assert dumptree(subroot) == SUBTREE.strip()

        touched_subroots = deeptrees.expand_tree(
            root=root, subroots=[subroot]
        )

        assert touched_subroots == ['B']
        assert dumptree(root) == FINAL_TREE.strip()


class TestSpecialCases(unittest.TestCase):

    def test_nested_root_not_expanded(self):

        root = Node('A')
        root.children = [Node('A')]

        touched_subroots = deeptrees.expand_tree(
            root=root, subroots=[root]
        )

        assert touched_subroots == []

    def test_subroot_inserted_once(self):

        root = make_primary_tree()

        subroot = Node('B')

        touched_roots = deeptrees.expand_tree(
            root=root, subroots=[subroot]
        )

        assert touched_roots == ['B']


class TestTreeCopier(unittest.TestCase):

    def test_copy_tree(self):

        root = make_primary_tree()
        twin = Node('A')

        deeptrees.TreeCopier().walk_to_copy_tree(root, twin)

        assert dumptree(root) == dumptree(twin)


if __name__ == '__main__':
    unittest.main()
