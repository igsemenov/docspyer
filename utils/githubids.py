# -*- coding: utf-8 -*-
"""Generates github style IDs for headings.
"""

import operator as opr
import collections


def makeids(headings) -> list[str]:
    """Generates github style IDs for a given list of headings.
    """
    idmaker = GitHubID()
    return idmaker.makeids(headings)


class GitHubID:
    """Maker of github style IDs.
    """

    def makeids(self, headings) -> list[str]:
        """Generates github style IDs for a given list of headings.

        Parameters
        ----------
        headings : list[str]
            Headings to be processed.

        Returns
        -------
        list[str]
            Github style IDs.

        """
        headings = self.edit_headings(headings)
        primary_ids = self.get_primary_ids(headings)
        return self.make_unique_ids(primary_ids)

    def edit_headings(self, headings):
        return list(
            map(self.edit_heading, headings)
        )

    def edit_heading(self, heading):
        return heading.replace('()', '')

    def get_primary_ids(self, headings: list[str]):

        def makeid(heading) -> str:
            return "-".join(
                heading.casefold().split()
            )

        return list(
            map(makeid, headings)
        )

    def make_unique_ids(self, keys) -> list[str]:

        if not keys:
            return []

        keys_are_unique = sorted(keys) == list(set(keys))

        if keys_are_unique:
            return list(keys)

        def ismulti(item):
            _, count = item
            return count > 1

        multis = filter(
            ismulti, collections.Counter(keys).items()
        )

        multikeys = map(
            opr.itemgetter(0), multis
        )

        for multikey in multikeys:
            keys = list(
                self.keys_enumerator(keys, targetkey=multikey)
            )

        return keys

    def keys_enumerator(self, keys, targetkey):
        """Adds an index number to the keys matching the target key.

        - The first match is skipped.
        - Further matches are numbered from 1.

        """
        count = 0
        for key in keys:
            if key == targetkey:
                if count:
                    yield key + f"-{count}"
                else:
                    yield key
                count += 1
            else:
                yield key
