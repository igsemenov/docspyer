# -*- coding: utf-8 -*-
"""Converts MD text to an HTML doc (object).
"""

import itertools as itr
import textwrap

from docspyer.utils import githubids
from docspyer.utils import texttrees
from docspyer.utils import treeashtml
from . import parser

__all__ = [
    'makedochtml'
]


def apiobj(obj):
    obj.__module__ = 'docspyer.docpage'
    return obj


@apiobj
def makedochtml(text):
    """Translates MD text to an HTML document.

    Parameters
    ----------
    text : str
        MD text to be translated.

    Returns
    -------
    DocHTML
        Object that holds the resulting HTML text and TOC
        as the attributes `text` and `toc`, respectively.

    Notes
    -----

    TOC features:

    - Build as an HTML list based on MD headings.
    - Contains ready-to-use links with github-style IDs.

    """
    docmaker = DocMaker()
    return docmaker.make_dochtml(text)


class DocHTML:
    """Represents an HTML document.

    Attributes
    ----------
    text : str
        Text of the document.
    toc : str
        TOC based on MD headings (links included).

    """

    def __init__(self, text, toc):
        self.text = text
        self.toc = toc


class DocMaker:
    """Converts an MD text to an HTML document.
    """

    def make_dochtml(self, text):

        if not text:
            return DocHTML('', '')

        blocks = self.get_blocks(text)

        headings = self.take_headings_from_blocks(blocks)
        toc = self.make_toc_from_headings(headings)
        text = self.dump_blocks_to_text(blocks)

        return self.make_instance(text, toc)

    def make_instance(self, text, toc):
        return DocHTML(text, toc)

    def make_toc_from_headings(self, headings):
        return TOCMaker().maketoc(headings)

    def get_blocks(self, text) -> list:
        return self.run_parser(text)

    def dump_blocks_to_text(self, blocks) -> str:
        return '\n\n'.join(
            [block.make_html() for block in blocks]
        )

    def run_parser(self, text) -> list:
        return parser.parsetext(text)

    def take_headings_from_blocks(self, blocks) -> list:
        def is_heading(block):
            return type(block).__name__ == 'MDHeading'
        return list(
            filter(is_heading, blocks)
        )


class TOCMaker:
    """Makes TOC from MD headings.

    - TOC is built as an HTML list with links as items.
    - Links include ready-to-use IDs in github format.

    """

    def maketoc(self, headings):

        if not headings:
            return ''

        toclist = self.make_toc_as_list(headings)
        treeroot = self.make_tree_from_list(toclist)

        return self.dump_tree_to_html(treeroot)

    def dump_tree_to_html(self, root):
        return treeashtml.dumptree_html(root)

    def make_tree_from_list(self, textlist):
        return texttrees.maketree(textlist)

    def make_toc_as_list(self, headings):

        links = self.get_links_with_githubdids(headings)

        levels = [
            heading.get_level() for heading in headings
        ]

        items = self.put_links_at_indents(links, levels)
        textlist = self.assemble(items)

        textlist = textwrap.dedent(textlist)
        return textlist

    def get_links_with_githubdids(self, headings):

        def make_atag(path, text):
            return f'<a href="#{path}">{text}</a>'

        texts = [
            heading.get_content() for heading in headings
        ]

        paths = githubids.makeids(texts)

        return list(
            itr.starmap(make_atag, zip(paths, texts))
        )

    def put_links_at_indents(self, links, levels):

        def add_listiter(item):
            return '- ' + item

        def indent_item(item, level):
            return '  '*(level-1) + item

        items = list(
            map(add_listiter, links)
        )

        items = list(
            itr.starmap(indent_item, zip(items, levels))
        )

        return items

    def assemble(self, items):
        return '\n'.join(items)
