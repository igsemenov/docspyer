# -*- coding: utf-8 -*-
"""Creates a combined TOC for a group of MD files.
"""

import re
import itertools as itr

from . import githubids
from . import texttrees
from . import treeashtml


def makemonotoc(sources) -> str:
    """Creates a monolithic TOC for a group of MD files.

    Parameters
    ----------
    sources : dict
        Namespace of source files (name-to-content).

    """
    maker = MonoContents()
    return maker.contents_from_sources(sources)


def makemultitoc(sources, level) -> str:
    """Creates a composite TOC for a group of MD files.

    Parameters
    ----------
    sources : dict
        Namespace of source files (name-to-content).
    level : int
        Level of the headings in the resulting TOC.

    """
    maker = MultiContents()
    return maker.contents_from_sources(sources, level)


class ContentsMaker:
    """Base class for contents makers.
    """

    def tocs_for_sources(self, sources) -> list[str]:

        tocmaker = self.make_toc_for_source
        name_text_pairs = sources.items()

        return list(
            itr.starmap(tocmaker, name_text_pairs)
        )

    def make_toc_for_source(self, filename, content):
        return self.run_toc_maker(filename, content)

    def run_toc_maker(self, filename, content):
        return TocMaker().make_toc(filename, content)

    def assemble(self, joint, items):
        return joint.join(items)

    def list_to_tree(self, listmd):
        return texttrees.maketree(listmd)

    def tree_to_html(self, root):
        return treeashtml.dumptree_html(root)


class MonoContents(ContentsMaker):
    """Makes a monolithic TOC for a group of MD files.
    """

    def contents_from_sources(self, sources):

        contents = self.contents_as_list(sources)
        contents = self.list_to_tree(contents)
        contents = self.tree_to_html(contents)

        return contents

    def contents_as_list(self, sources):

        tocs = self.tocs_for_sources(sources)

        return self.assemble(
            joint='\n', items=tocs
        )


class MultiContents(ContentsMaker):
    """Makes a composite TOC for a group of MD files.
    """

    def contents_from_sources(self, sources, level):

        sections = self.make_sections(sources, level)

        return self.assemble(
            joint='\n\n', items=sections
        )

    def make_sections(self, sources, level):
        tocs = self.make_tocs(sources)
        headings = self.make_headings(sources, level)
        return self.combine(tocs, headings)

    def combine(self, tocs, headings):

        def merge(toc, heading):
            return heading + '\n\n' + toc

        return list(
            itr.starmap(merge, zip(tocs, headings))
        )

    def make_tocs(self, sources):
        tocs = self.tocs_for_sources(sources)
        return self.tocs_to_html(tocs)

    def tocs_to_html(self, tocs):

        converter = self.toc_to_html

        return list(
            map(converter, tocs)
        )

    def toc_to_html(self, toc):
        root = self.list_to_tree(toc)
        return self.tree_to_html(root)

    def make_headings(self, sources, level):

        prefix = '#'*level + ' '

        def getheading(name):
            return prefix + name

        filenames = sources.keys()

        return list(
            map(getheading, filenames)
        )


class TocMaker:
    """Makes TOC for a single MD file.

    - TOC is an MD list with HTML links.
    - Links are to `FILENAME.md#HEADING-ID`.

    """

    RE_HEADING = '#{1,} '

    def __init__(self):
        self._filename = None

    def make_toc(self, filename, source) -> str:

        self._filename = filename

        headings = self.fetch_headings(source)
        toc = self.toc_from_headings(headings)

        return toc

    def toc_from_headings(self, headings) -> str:
        ids = self.make_github_ids(headings)
        items = self.make_items(headings, ids)
        return self.assemble(items)

    def make_github_ids(self, headings):

        texts = [
            heading.lstrip('# ') for heading in headings
        ]

        return githubids.makeids(texts)

    def make_items(self, headings, ids):
        return itr.starmap(
            self.item_for_heading, zip(headings, ids)
        )

    def item_for_heading(self, heading, githubid):

        level = heading.count('#')
        text = heading.lstrip('# ')

        link = self.html_link_for_heading(text, githubid)

        prefix = 2*(level-1)*chr(32)
        return prefix + '- ' + link

    def html_link_for_heading(self, text, githubid):
        path = f'{self._filename}.md#{githubid}'
        return f'<a href="{path}">{text}</a>'

    def fetch_headings(self, text) -> list[str]:
        pars = self.fetchpars(text)
        return self.filter_headings(pars)

    def filter_headings(self, pars) -> list[str]:

        return list(
            filter(self.is_heading, pars)
        )

    def fetchpars(self, text) -> list[str]:

        pars = re.split('\n\s{0,}\n', text)

        return list(
            filter(len, map(str.strip, pars))
        )

    def is_heading(self, text):
        if text.count('\n') > 0:
            return False
        if re.match(self.RE_HEADING, text):
            return True
        return False

    def assemble(self, items):
        return '\n'.join(items)
