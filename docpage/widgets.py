# -*- coding: utf-8 -*-
"""Docpage widgets as SVG tags.
"""

from .getsvg import svgtag, shapes


class Contents(svgtag.SVG):
    """Global TOC button.

    - Rounded box with 3 horizontal stripes (circle+line).

    """

    def maketag(self, width=25, height=25):

        viewbox = self.set_viewbox()
        content = self.get_content()

        return self.render_svgtag(
            content, 'svg-widget', width, height, viewbox
        )

    def get_content(self):
        return getattr(self, 'make_content')()

    def set_viewbox(self):
        return [0, 0, 30, 30]

    def make_content(self):

        box = self.render_box()
        stripes = self.render_stripes()

        return self.assemble(
            box, stripes
        )

    def render_box(self):
        return shapes.Rect().render(
            top_left_x=0, top_left_y=0, width=30, height=30, radius=7
        )

    def render_stripes(self):
        lines = self.render_lines()
        circles = self.render_circs()
        return self.assemble(circles, lines)

    def render_circs(self):

        generator = self.gencircs
        renderer = self.render_gtag

        circles = generator(
            start_x=7, start_y=8, stepy=7, radius=2
        )

        return renderer(
            content='\n'.join(circles), attrs={'fill': 'white'}
        )

    def render_lines(self):

        generator = self.genlines
        renderer = self.render_gtag

        lines = generator(
            start_x=12, start_y=8, stepy=7, length=13
        )

        attrs = {
            'stroke': 'white',
            'stroke-width': '3'
        }

        return renderer(
            content='\n'.join(lines), attrs=attrs
        )

    def gencircs(self, start_x, start_y, stepy, radius):

        circ = shapes.Circ()

        center_x = start_x
        center_y = start_y

        for _ in range(3):

            yield circ.render(
                center_x, center_y, radius
            )

            center_y += stepy

    def genlines(self, start_x, start_y, stepy, length):

        line = shapes.Line()

        for _ in range(3):

            yield line.render(
                start_x, start_y, start_x+length, start_y
            )

            start_y += stepy


class Bookmark(svgtag.SVG):
    """Local TOC button.

    - Rounded bookmark-like box with 2 horizontal stripes.

    """

    def maketag(self, width=25, height=25):

        viewbox = self.set_viewbox()
        content = self.get_content()

        return self.render_svgtag(
            content, 'svg-widget', width, height, viewbox
        )

    def set_viewbox(self):
        return [0, 0, 30, 30]

    def get_content(self):
        return getattr(self, 'make_content')()

    def make_content(self):
        box = self.render_box()
        stripes = self.render_stripes()
        return self.assemble(box, stripes)

    def render_box(self):
        top = self.render_box_top()
        bottom = self.render_box_bottom()
        return self.assemble(top, bottom)

    def render_box_top(self):
        return shapes.Rect().render(
            top_left_x=1, top_left_y=1, width=28, height=20, radius=7
        )

    def render_box_bottom(self):
        return shapes.Path().render(
            definition="M 1 10 v 20 q 14 -7 28 0 v -20"
        )

    def render_stripes(self):

        generator = self.genlines
        renderer = self.render_gtag

        lines = generator(
            start_x=9, start_y=10, stepy=7, length=12
        )

        attrs = {
            'stroke': 'white',
            'stroke-width': '3',
            'stroke-linecap': 'round'
        }

        return renderer(
            content='\n'.join(lines), attrs=attrs
        )

    def genlines(self, start_x, start_y, stepy, length):

        line = shapes.Line()

        for _ in range(2):

            yield line.render(
                start_x, start_y, start_x+length, start_y
            )

            start_y += stepy


class Homepage(svgtag.SVG):
    """Homepage button.

    - Box with a triangle roof and a rectangular door.

    """

    def maketag(self, width=30, height=25):

        viewbox = self.set_viewbox()
        content = self.get_content()

        return self.render_svgtag(
            content, 'svg-widget', width, height, viewbox
        )

    def set_viewbox(self):
        return [0, 0, 36, 30]

    def get_content(self):
        return getattr(self, 'make_content')()

    def make_content(self):

        box = self.render_box()
        roof = self.render_roof()
        door = self.render_door()

        return self.assemble(box, roof, door)

    def render_box(self):
        top = self.render_box_top()
        bottom = self.render_box_bottom()
        return self.assemble(top, bottom)

    def render_box_top(self):
        return shapes.Rect().render(
            top_left_x=6, top_left_y=10, width=24, height=10, radius=0
        )

    def render_box_bottom(self):
        return shapes.Rect().render(
            top_left_x=6, top_left_y=15, width=24, height=15, radius=2
        )

    def render_roof(self):

        attrs = {
            'stroke-width': '3',
            'stroke-linecap': 'round',
            'stroke-linejoin': 'round'
        }

        definition = "M 18 2 l 16 10 l -16 0 l -16 0 l 16 -10"
        return shapes.Path().render(definition, attrs)

    def render_door(self):
        return shapes.Rect().render(
            top_left_x=15, top_left_y=20,
            width=6, height=10, radius=0, attrs={'fill': 'white'}
        )
