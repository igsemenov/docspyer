# -*- coding: utf-8 -*-
"""Simple editor of inline MD patterns.
"""

import re


def edit_inline_md(text) -> str:
    """Translates inline MD patterns to HTML.
    """
    editor = InlineEditor()
    return editor.edit_text(text)


class InlineEditor:

    RE_PATTERN = '[\s>]S{1,}[^S]+S{1,}[\s,.:<]'

    RE_WITH_BACKTICKS = re.compile(
        RE_PATTERN.replace('S', '`')
    )

    RE_WITH_QUOTMARKS = re.compile(
        RE_PATTERN.replace('S', '"')
    )

    RE_WITH_ASTERISKS = re.compile(
        RE_PATTERN.replace('S', '\*')
    )

    RE_LINK_NAME = '[.\w\s]{1,}(\(\w*\)){0,1}'
    RE_LINK_PATH = '[\w.#-]{0,}'

    RE_LINK = "\s\[NAME\]\(PATH\)[\s,.:]"

    RE_LINK = RE_LINK.replace('NAME', RE_LINK_NAME)
    RE_LINK = RE_LINK.replace('PATH', RE_LINK_PATH)

    def edit_text(self, text):

        text = self.edit_quotmarks(text)
        text = self.edit_backticks(text)
        text = self.edit_asterisks(text)
        text = self.edit_links(text)

        return text

    def edit_backticks(self, text):
        return getattr(self, 'edit_pattern')(
            text, self.RE_WITH_BACKTICKS, self.translate_backticks
        )

    def edit_quotmarks(self, text):
        return getattr(self, 'edit_pattern')(
            text, self.RE_WITH_QUOTMARKS, self.translate_quotmarks
        )

    def edit_asterisks(self, text):
        return getattr(self, 'edit_pattern')(
            text, self.RE_WITH_ASTERISKS, self.translate_asterisks
        )

    def edit_links(self, text):
        return getattr(self, 'edit_pattern')(
            text, self.RE_LINK, self.translate_link
        )

    def translate_backticks(self, snippet):
        return self.edit_snippet(
            snippet, symbol='`', start='<code>', end='</code>'
        )

    def translate_quotmarks(self, snippet):
        return self.edit_snippet(
            snippet, symbol='"', start='<i>&quot;', end='&quot;</i>'
        )

    def translate_asterisks(self, snippet):
        if snippet.count('*') == 4:
            return self.translate_bold(snippet)
        if snippet.count('*') == 2:
            return self.translate_italic(snippet)
        if snippet.count('*') == 6:
            return self.translate_bold_italic(snippet)
        return snippet

    def translate_bold_italic(self, snippet):
        return self.edit_snippet(
            snippet, symbol='***', start='<b><em>', end='</em></b>'
        )

    def translate_bold(self, snippet):
        return self.edit_snippet(
            snippet, symbol='**', start='<b>', end='</b>'
        )

    def translate_italic(self, snippet):
        return self.edit_snippet(
            snippet, symbol='*', start='<em>', end='</em>'
        )

    def translate_link(self, snippet):
        return LinkEditor().convert_link(snippet)

    def edit_snippet(self, snippet, symbol, start, end):
        snippet = snippet.replace(symbol, start, 1)
        snippet = snippet.replace(symbol, end, 1)
        return snippet

    def edit_pattern(self, text, re_with_pattern, translator):

        text = ' ' + text + ' '

        for obj in re.finditer(re_with_pattern, text):

            snippet = obj.group()

            text = text.replace(
                snippet, translator(snippet)
            )

        return text[1:-1]


class LinkEditor:
    """Converts MD links to HTML ones.
    """

    RE_PATH = re.compile(
        "\]\(PATH\)".replace('PATH', InlineEditor.RE_LINK_PATH)
    )

    RE_NAME = re.compile(
        "\[NAME\]\(".replace('NAME', InlineEditor.RE_LINK_NAME)
    )

    def convert_link(self, snippet):

        name = self.fetch_name(snippet)
        path = self.fetch_path(snippet)

        newlink = self.make_html_link(name, path)
        oldlink = f'[{name}]({path})'

        return snippet.replace(oldlink, newlink)

    def fetch_path(self, snippet):
        matchobj = self.RE_PATH.search(snippet)
        return matchobj.group().strip(']()')

    def fetch_name(self, snippet):
        matchobj = self.RE_NAME.search(snippet)
        return matchobj.group().strip('[](')

    def make_html_link(self, name, path):
        return f'<a href="{path}">{name}</a>'
