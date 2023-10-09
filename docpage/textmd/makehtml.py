# -*- coding: utf-8 -*-
"""Converts MD text to an HTML document.
"""

import itertools as itr
import textwrap

from docspy.utils import githubids
from docspy.utils import texttrees
from docspy.utils import treeashtml
from . import parser


def makedochtml(text) -> str:
    """Translates MD text to an HTML document.

    Parameters
    ----------
    text : str
        MD text to be translated.

    Returns
    -------
    DocHTML
        Object that holds the resulting HTML text with TOC.

    """
    docmaker = DocMaker()
    return docmaker.makedoc(text)


class DocHTML:
    """Represents an HTML document.

    Attributes
    ----------
    text : str
        Text of the document.
    toc : str
        Table of contents based on headings (links included).

    """

    def __init__(self, text, toc):
        self.text = text
        self.toc = toc


class DocMaker:
    """Converts an MD text to an HTML document.
    """

    def __init__(self):
        self.set_tocmaker()

    def set_tocmaker(self):
        self.tocmaker = TOCMaker()

    def makedoc(self, text):

        if not text:
            return DocHTML('', '')

        blocks = self.get_blocks(text)

        headings = self.fetch_headings_from_blocks(blocks)
        toc = self.make_toc_from_headings(headings)
        text = self.dump_blocks_to_text(blocks)

        return self.make_doc_html(text, toc)

    def make_doc_html(self, text, toc):
        return DocHTML(text, toc)

    def make_toc_from_headings(self, headings):
        toc_maker = self.tocmaker.maketoc
        return toc_maker(headings)

    def get_blocks(self, text) -> list:
        return self.run_parser(text)

    def dump_blocks_to_text(self, blocks) -> str:
        return '\n\n'.join(
            [block.make_html() for block in blocks]
        )

    def run_parser(self, text) -> list:
        return parser.parsetext(text)

    def fetch_headings_from_blocks(self, blocks) -> list:
        def is_heading(block):
            return type(block).__name__ == 'MDHeading'
        return list(
            filter(is_heading, blocks)
        )


class TOCMaker:
    """Makes table of contents (TOC) from a list of headings.
    """

    def maketoc(self, headings):

        if not headings:
            return ''

        toc_as_textlist = self.make_toc_as_text_list(headings)
        treeroot = self.make_tree_from_text_list(toc_as_textlist)

        return self.dump_tree_to_html_list(treeroot)

    def dump_tree_to_html_list(self, root):
        return treeashtml.dumptree_html(root)

    def make_tree_from_text_list(self, textlist):
        return texttrees.maketree(textlist)

    def make_toc_as_text_list(self, headings):

        links = self.make_links_with_githubdids(headings)

        levels = [
            heading.get_level() for heading in headings
        ]

        items = self.arrange_links_as_list_items(links, levels)
        textlist = self.assemble_items(items)

        textlist = textwrap.dedent(textlist)
        return textlist

    def make_links_with_githubdids(self, headings):

        def make_atag(path, text):
            return f'<a href="#{path}">{text}</a>'

        texts = [
            heading.get_content() for heading in headings
        ]

        paths = githubids.makeids(texts)

        return list(
            itr.starmap(make_atag, zip(paths, texts))
        )

    def arrange_links_as_list_items(self, links, levels):

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

    def assemble_items(self, items):
        return '\n'.join(items)
