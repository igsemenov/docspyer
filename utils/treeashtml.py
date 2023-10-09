# -*- coding: utf-8 -*-
"""Prints a tree as an HTML list.
"""

import textwrap
from . import treeprinter


def dumptree_html(root, indent=4) -> str:
    """Renders a tree as an HTML list.

    Parameters
    ----------
    root : node-like
        Root of the tree to be printed.
    indent : int
        Number of spaces per indentation level.

    """
    tree_printer = TreePrinter()
    tree_printer.set_indent(indent)
    return tree_printer.make_tree_view(root)


class TreePrinter(treeprinter.TreePrinter):

    def set_node_printer(self):
        self.node_printer = NodePrinter()

    def set_indent(self, indent):
        self.node_printer.set_indent(indent)

    def finalize_root_view(self, root):

        view = root.view

        view = self.dedent_tag_body(view)
        view = self.change_tag_to_ptag(view)

        return view

    def dedent_tag_body(self, text) -> str:

        lines = text.splitlines()

        bodylines = lines[1:-1]
        bodytext = '\n'.join(bodylines)
        newbodytext = textwrap.dedent(bodytext)

        return '\n'.join(
            [lines[0], newbodytext, lines[-1]]
        )

    def change_tag_to_ptag(self, text) -> str:

        lines = text.splitlines()

        firstline = lines[0].replace('<li>', '<p>')
        lastline = lines[-1].replace('</li>', '</p>')

        return '\n'.join(
            [firstline, *lines[1:-1], lastline]
        )


class NodePrinter(treeprinter.NodePrinter):

    def __init__(self):
        self.indent = None

    def set_indent(self, indent):
        self.indent = chr(32)*indent

    def render_data(self, node) -> str:
        content = self.text_to_line(node.data)
        return self.make_li_tag_as_line(content)

    def render_children(self, node) -> str:
        view = self.dump_views_and_indent(node.children)
        view = self.make_ul_tag_as_block(view)
        return view

    def assemble_node_view(self, nodeview, childrenview):

        indenttext = self.indent_text
        content = indenttext(childrenview)

        view = nodeview.replace(
            '</li>', '\n' + content + '\n</li>'
        )

        return view

    def dump_views_and_indent(self, nodes) -> str:

        indenttext = self.indent_text

        views = [
            node.view for node in nodes
        ]

        view = '\n'.join(views)
        return indenttext(view)

    def indent_text(self, text):
        return textwrap.indent(
            text=text, prefix=self.indent
        )

    def make_li_tag_as_line(self, content) -> str:
        tagmaker = self.make_a_tag
        return tagmaker('li', content, asblock=False)

    def make_ul_tag_as_block(self, content) -> str:
        tagmaker = self.make_a_tag
        return tagmaker('ul', content, asblock=True)

    def make_a_tag(self, name, content, asblock) -> str:
        return '<{0}>{2}{1}{2}</{0}>'.format(
            name, content, '\n' if asblock is True else ''
        )
