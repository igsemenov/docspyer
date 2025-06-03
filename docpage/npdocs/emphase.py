# -*- coding: utf-8 -*-
"""Editor of inline MD patterns in docstrings.
"""

import re
from ..textmd.emphase import edit_inline_md


def emphasize(text) -> str:
    """Emphasizes keywords and inline MD in text.
    """
    editor = InlineEditor()
    return editor.emphasize_text(text)


class InlineEditor:

    KEYWORDS = (
        "True", "False", "None"
    )

    RE_KEYWORDS = "(" + "|".join(KEYWORDS) + ")"

    RE_WITH_KEYWORD = re.compile(
        r"\W" + RE_KEYWORDS + r"\W"
    )

    def emphasize_text(self, text) -> str:

        text = self.emphasize_keywords(text)
        text = self.emphasize_inlinemd(text)

        return text

    def emphasize_keywords(self, text) -> str:

        re_keywords = self.RE_KEYWORDS
        re_with_keyword = self.RE_WITH_KEYWORD

        def repl_keyword(obj):
            return "<em>" + obj.group() + "</em>"

        def repl_snippet(obj):
            return re.sub(
                re_keywords, repl_keyword, obj.group()
            )

        text = ' ' + text + ' '

        text = re.sub(
            re_with_keyword, repl_snippet, text
        )

        return text[1:-1]

    def emphasize_inlinemd(self, text):
        return edit_inline_md(text)
