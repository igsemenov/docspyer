# -*- coding: utf-8 -*-
"""Base class for tree printers.
"""


class TreeNode:
    """Minimum required node model.

    Attributes
    ----------
    data : str
        Text data to be printed.
    children : list | None
        Children nodes.

    """


class TreePrinter:
    """Base class for tree printers.
    """

    def __init__(self):
        self.set_node_printer()

    def set_node_printer(self):
        self.node_printer = NodePrinter()

    def make_tree_view(self, root) -> str:
        self.walk_and_build_views(root)
        view = self.finalize_root_view(root)
        self.walk_and_clear_views(root)
        return view

    def walk_and_build_views(self, root):
        getattr(self, 'walk_to_build_views')(root)

    def walk_and_clear_views(self, root):
        getattr(self, 'walk_to_clear_views')(root)

    def walk_to_build_views(self, node):

        if not node.children:
            node.view = self.dump_leaf_node(node)
            return

        for child in node.children:
            self.walk_to_build_views(child)

        node.view = self.dump_body_node(node)
        return

    def dump_body_node(self, node):
        nodeprinter = self.node_printer
        return nodeprinter.dump_body_node(node)

    def dump_leaf_node(self, node):
        nodeprinter = self.node_printer
        return nodeprinter.dump_leaf_node(node)

    def walk_to_clear_views(self, node):

        self.clear_node_view(node)

        if not node.children:
            return

        for child in node.children:
            self.walk_to_clear_views(child)

    def clear_node_view(self, node):
        if hasattr(node, 'view'):
            del node.view

    def finalize_root_view(self, root) -> str:
        return root.view


class NodePrinter:
    """Base class for node printers.
    """

    def dump_leaf_node(self, node) -> str:
        return self.render_data(node)

    def dump_body_node(self, node) -> str:

        nodeview = self.render_data(node)
        childrenview = self.render_children(node)

        return self.assemble_node_view(
            nodeview, childrenview
        )

    def render_data(self, node) -> str:
        """TBD in derived classes.
        """
        return node.data

    def render_children(self, node) -> str:
        """TBD in derived classes.
        """

        views = [
            child.view for child in node.children
        ]

        return '\n'.join(views)

    def assemble_node_view(self, nodeview, childrenview) -> str:
        """TBD in derived classes.
        """
        return '\n'.join(
            [nodeview, childrenview]
        )

    def text_to_line(self, text) -> str:
        words = self.fetch_words(text)
        return self.align_words(words)

    def fetch_words(self, text) -> list[str]:
        return text.split()

    def align_words(self, words) -> str:
        return chr(32).join(words)
