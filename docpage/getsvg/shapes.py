# -*- coding: utf-8 -*-
"""Basic SVG shapes.
"""


class Shape:
    """Base class for SVG shapes.
    """

    NAME = None
    PARAMS = None

    def format_template(self, *params, attrs=None):

        template = self.get_template()

        shapeview = self.insert_params(template, *params)
        shapeview = self.insert_attrs(shapeview, attrs)

        return shapeview

    def insert_params(self, template, *params):
        return template.format(*params)

    def insert_attrs(self, shapeview, attrs: dict):

        renderer = self.render_attrs

        attrs_view = renderer(attrs)
        attrs_view = str.rstrip(' ' + attrs_view)

        return shapeview.replace(
            '/>', attrs_view + '/>'
        )

    def get_template(self):

        make_params_template = self.get_params_placeholders

        name = self.NAME
        params = make_params_template()

        return f'<{name} {params}/>'

    def get_params_placeholders(self) -> str:

        names = self.PARAMS
        renderer = self.render_attrs

        param_templates = {
            name: '{' + str(i) + '}' for i, name in enumerate(names)
        }

        return renderer(param_templates)

    def render_attrs(self, attrs: dict) -> str:

        if not attrs:
            return ''

        views = [
            f'{key}="{val}"' for key, val in attrs.items()
        ]

        return chr(32).join(views)


class Rect(Shape):

    NAME = 'rect'
    PARAMS = 'x', 'y', 'width', 'height', 'rx'

    def render(self,
               top_left_x, top_left_y, width, height, radius, attrs=None):

        return self.format_template(
            top_left_x, top_left_y, width, height, radius, attrs=attrs
        )


class Circ(Shape):

    NAME = 'circle'
    PARAMS = 'cx', 'cy', 'r'

    def render(self, center_x, center_y, radius, attrs=None):

        return self.format_template(
            center_x, center_y, radius, attrs=attrs
        )


class Line(Shape):

    NAME = 'line'
    PARAMS = 'x1', 'y1', 'x2', 'y2'

    def render(self, start_x, start_y, end_x, end_y, attrs=None):

        return self.format_template(
            start_x, start_y, end_x, end_y, attrs=attrs
        )


class Path(Shape):

    NAME = 'path'
    PARAMS = ('d',)

    def render(self, definition, attrs=None):

        return self.format_template(
            definition, attrs=attrs
        )
