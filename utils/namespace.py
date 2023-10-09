# -*- coding: utf-8 -*-
"""Basic operations with name-to-names mappings.
"""

from . import treeastxt


def dumpnamespace(name_to_names, rootname=None) -> str:
    """Returns a tree-like view of the name-to-names mapping.
    """

    if not name_to_names:
        return ''

    root = namespace_to_tree(name_to_names, rootname)

    return run_treeprinter(root)


def run_treeprinter(root):
    return treeastxt.dumptree_txt(root)


def namespace_to_tree(name_to_names, rootname=None):
    """Represents the namespace as a tree.
    """

    Node = TreeNode

    def item_as_tree(name, names):
        root = Node(name)
        root.children = [
            Node(name) for name in names
        ]
        return root

    root = Node(rootname)

    root.children = [
        item_as_tree(name, names) for name, names in name_to_names.items()
    ]

    return root


def invertmap(name_to_names) -> dict:
    """Inverts the name-to-names mapping.
    """

    set_of_values = set()
    for value in name_to_names.values():
        set_of_values.update(value)

    value_to_keys = {
        value: [] for value in set_of_values
    }

    for key, values in name_to_names.items():
        for value in values:
            if key not in value_to_keys[value]:
                value_to_keys[value].append(key)

    return value_to_keys


def exclude_non_native_names(name_to_names) -> dict:
    """Remove values (names) that are not in the set of keys.
    """

    native_names = name_to_names.keys()

    def is_native_name(name):
        return name in native_names

    def filter_non_native_names(names):
        return list(
            filter(is_native_name, names)
        )

    items = name_to_names.items()

    return {
        name: filter_non_native_names(names) for name, names in items
    }


class TreeNode:

    def __init__(self, data):
        self.data = data
        self.children = None
