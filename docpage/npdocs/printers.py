# -*- coding: utf-8 -*-
"""Printers of docstring blocks.
"""

import textwrap
from . import emphase


class BasePrinter:
    """Base class for printers.
    """

    PREFIX = 3*chr(32)

    def emphasize(self, text) -> str:
        return emphase.emphasize(text)

    def dump_as_it_is(self, text):
        return text

    def dump_indented(self, text):
        return textwrap.indent(
            text, prefix=self.PREFIX
        )

    def dump_as_bold_html(self, text):
        return '<b>' + text + '</b>'

    def dump_as_bold_md_rst(self, text):
        return '**' + text + '**'

    def dump_as_rst_rubric(self, text):
        return f'.. rubric:: {text}'

    def dump_as_raw_html_rst(self, text):

        indentblock = self.dump_indented

        parts = [
            '.. raw:: html', indentblock(text)
        ]

        return '\n\n'.join(parts)


class TextPrinter(BasePrinter):

    def printblock(self, block):
        return self.render_content(block.content)

    def render_content(self, content):
        return content


class TextPrinterMD(TextPrinter):

    def render_content(self, content):
        return self.dump_as_it_is(content)


class TextPrinterRST(TextPrinter):

    def render_content(self, content):
        return self.dump_as_it_is(content)


class SectionPrinter(BasePrinter):

    def printblock(self, block):
        heading = self.render_heading(block.heading)
        content = self.render_content(block.content)
        return self.assemble(heading, content)

    def render_heading(self, heading):
        return heading

    def render_content(self, content):
        return content

    def assemble(self, heading, content) -> str:
        return '\n\n'.join(
            filter(len, [heading, content])
        )


class SectionPrinterMD(SectionPrinter):

    def render_heading(self, heading) -> str:
        return self.dump_as_bold_html(heading)

    def render_content(self, content) -> str:
        return self.emphasize(content)


class SectionPrinterRST(SectionPrinter):

    def render_heading(self, heading) -> str:
        return self.dump_as_bold_md_rst(heading)

    def render_content(self, content) -> str:
        return self.dump_as_it_is(content)


class VarlistPrinter(BasePrinter):

    def __init__(self):
        self.set_varprinter()

    def set_varprinter(self):
        self.varprinter = VarPrinter()

    def printblock(self, block):
        heading = self.render_heading(block.heading)
        variables = self.render_variables(block.variables)
        variables = self.format_variables(variables)
        return self.assemble(heading, variables)

    def render_heading(self, heading):
        return heading

    def render_variables(self, varrecords) -> str:

        if not varrecords:
            return ''

        return '\n\n'.join(
            map(self.varprinter.printvar, varrecords)
        )

    def format_variables(self, variables):
        return variables

    def assemble(self, heading, content) -> str:
        return '\n\n'.join(
            filter(len, [heading, content])
        )


class VarlistPrinterMD(VarlistPrinter):

    def render_heading(self, heading) -> str:
        return self.dump_as_bold_html(heading)

    def format_variables(self, variables):
        return self.dump_as_it_is(variables)


class VarlistPrinterRST(VarlistPrinter):

    def render_heading(self, heading):
        return self.dump_as_bold_md_rst(heading)

    def format_variables(self, variables):

        if not variables:
            return ''

        return self.dump_as_raw_html_rst(variables)


class VarPrinter:

    VARSYMB = ''

    def printvar(self, varrec) -> str:

        vardef = self.render_vardef(
            varrec.varname, varrec.vartype
        )

        vardoc = self.render_vardoc(varrec.vardoc)

        return '\n\n'.join(
            [vardef, vardoc]
        )

    def render_vardoc(self, vardoc) -> str:
        vardoc = self.emphasize(vardoc)
        vardoc = self.dedent_indent(vardoc)
        return self.dump_to_details_tag(vardoc)

    def render_vardef(self, varname, vartype) -> str:
        vardef = self.make_vardef(varname, vartype)
        return self.format_vardef(vardef)

    def make_vardef(self, varname, vartype):

        varname = self.render_varname(varname)
        vartype = self.render_vartype(vartype)

        vardef = ' : '.join(
            filter(len, [varname, vartype])
        )

        vardef = self.handle_no_type(vardef)
        return vardef

    def format_vardef(self, vardef):
        vardef = self.put_into_span(vardef)
        vardef = self.put_into_ptag(vardef)
        return vardef

    def handle_no_type(self, vardef):

        if ' : ' in vardef:
            return vardef

        vardef = vardef.removeprefix(self.VARSYMB)
        vardef = vardef.replace('<code>', '<em>')
        vardef = vardef.replace('</code>', '</em>')

        return vardef

    def render_varname(self, varname):
        if not varname:
            return ''
        return self.VARSYMB + f'<code>{varname}</code>'

    def render_vartype(self, vartype):
        if not vartype:
            return ''
        return '<em>' + vartype + '</em>'

    def dump_to_details_tag(self, text) -> str:
        return f'<dl><dd>\n{text}\n</dd></dl>'

    def dedent_indent(self, text):
        dedenter = self.dedent_text
        indenter = self.indent_text
        return indenter(dedenter(text))

    def emphasize(self, text) -> str:
        return emphase.emphasize(text)

    def dedent_text(self, text) -> str:
        return '\n'.join(
            [line.lstrip() for line in text.splitlines()]
        )

    def indent_text(self, text, indent=2):
        prefix = ' '*indent
        return '\n'.join(
            [prefix + line for line in text.splitlines()]
        )

    def put_into_ptag(self, text):
        return f'<p>{text}</p>'

    def put_into_span(self, text):
        return f'<span class="vardef">{text}</span>'
