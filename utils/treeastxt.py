# -*- coding: utf-8 -*-
"""Prints a tree in plain text.
"""

from . import treeprinter


def dumptree_txt(root) -> str:
    """Renders a tree view in plain text.
    """
    tree_printer = TreePrinter()
    return tree_printer.make_tree_view(root)


class TreePrinter(treeprinter.TreePrinter):

    rootsign = '• '

    def set_node_printer(self):
        self.node_printer = NodePrinter()

    def finalize_root_view(self, root) -> str:

        blank_padding = chr(32)*len(self.rootsign)

        def editlines(lines):
            for count, line in enumerate(lines):
                if count == 0:
                    yield self.rootsign + line
                else:
                    yield blank_padding + line

        old_lines = root.view.splitlines()
        new_lines = editlines(old_lines)

        return '\n'.join(new_lines)


class NodePrinter(treeprinter.NodePrinter):

    fakenode = '+'

    def __init__(self):
        self.set_children_printer()

    def set_children_printer(self):
        self.children_printer = ChildrenPrinter()

    def render_data(self, node) -> str:
        fakenode = self.fakenode_if_no_data(node)
        textdata = self.data_as_line_if_data(node)
        return fakenode or textdata

    def fakenode_if_no_data(self, node) -> str:
        if not node.data:
            return self.fakenode
        return ''

    def data_as_line_if_data(self, node) -> str:
        if node.data:
            return self.text_to_line(node.data)
        return ''

    def render_children(self, node) -> str:
        return self.children_printer.render_children(node)


class ChildrenPrinter:

    vertline = '│  '
    bodynode = '├─ '
    lastnode = '└─ '

    def render_children(self, node) -> str:

        if not node.children:
            return ''

        lastchild = node.children[-1]
        mostchildren = node.children[:-1]

        mostviews = self.render_most_children(mostchildren)
        lastview = self.render_last_child(lastchild)

        new_views = [
            *mostviews, lastview
        ]

        return self.assemble(*new_views)

    def render_most_children(self, mostchildren) -> list[str]:

        printer = self.render_bulk_child

        return [
            printer(child) for child in mostchildren
        ]

    def render_bulk_child(self, child) -> str:

        def editlines(lines):
            for count, line in enumerate(lines):
                if count == 0:
                    yield self.bodynode + line
                else:
                    yield self.vertline + line

        new_lines = editlines(
            child.view.splitlines()
        )

        return '\n'.join(new_lines)

    def render_last_child(self, child) -> str:

        blank_padding = chr(32)*len(self.lastnode)

        def editlines(lines):
            for count, line in enumerate(lines):
                if count == 0:
                    yield self.lastnode + line
                else:
                    yield blank_padding + line

        new_lines = editlines(
            child.view.splitlines()
        )

        return '\n'.join(new_lines)

    def assemble(self, *parts):
        return '\n'.join(parts)
