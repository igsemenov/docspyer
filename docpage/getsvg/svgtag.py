# -*- coding: utf-8 -*-
"""Base class for SVG tags.
"""

import textwrap


class SVG:
    """Base class for SVG tags.
    """

    def render_svgtag(self, content, classcss: str,
                      width, height, viewbox, attrs: dict = None):

        if not content:
            return ''

        viewboxstr = str(viewbox)
        viewboxstr = viewboxstr.replace(',', '').strip('[]')

        params = {
            'class': classcss,
            'width': str(width),
            'height': str(height),
            'viewbox': viewboxstr
        }

        attrs = attrs or {}
        all_attrs = params | attrs

        attrstr = self.render_attrs(all_attrs)
        content = textwrap.indent(content, prefix='  ')

        return f'<svg {attrstr}>\n{content}\n</svg>'

    def render_gtag(self, content, attrs: dict = None):

        if not content:
            return ''

        attrstr = self.render_attrs(
            attrs or {}
        )

        content = textwrap.indent(
            content, prefix='  '
        )

        return f'<g {attrstr}>\n{content}\n</g>'

    def render_attrs(self, attrs: dict) -> str:

        if not attrs:
            return ''

        views = [
            f'{key}="{val}"' for key, val in attrs.items()
        ]

        return chr(32).join(views)

    def assemble(self, *parts):
        return '\n'.join(
            filter(len, parts)
        )

    def connect(self, *parts):
        return chr(32).join(
            filter(len, parts)
        )
