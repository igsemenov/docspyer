# -*- coding: utf-8 -*-
"""Structural blocks of numpy style docstrings.
"""

from . import printers


class Block:
    """Base class for blocks of numpy style docstrings.
    """

    PRINTER_MD = None
    PRINTER_RST = None

    def is_section(self):
        return isinstance(self, Section)

    def is_varlist(self):
        return isinstance(self, Varlist)

    def is_textdata(self):
        return isinstance(self, Textdata)

    def is_block(self):
        return isinstance(
            self, (Section, Varlist, Textdata)
        )

    def render_md(self):
        return self.run_printer_md()

    def render_rst(self):
        return self.run_printer_rst()

    def run_printer_md(self):
        return self.PRINTER_MD.printblock(self)

    def run_printer_rst(self):
        return self.PRINTER_RST.printblock(self)


class Textdata(Block):
    """An ordinary paragraph with some text data.

    Attributes
    ----------
    content : str
        Content of the block.

    """

    PRINTER_MD = printers.TextPrinterMD()
    PRINTER_RST = printers.TextPrinterRST()

    def __init__(self, text):
        self.content = text


class Section(Block):
    """A paragraph with a heading.

    Attributes
    ----------
    heading : str
        Section heading.
    content : str
        Section text.

    """

    headings = (
        'Notes',
        'Examples',
        'See Also'
    )

    PRINTER_MD = printers.SectionPrinterMD()
    PRINTER_RST = printers.SectionPrinterRST()

    def __init__(self, heading, content):
        self.heading = heading
        self.content = content


class Varlist(Block):
    """A paragraph that contains a variable list.

    Attributes
    ----------
    heading : str
        Heading of the list.
    variables : list[VarRecord]
        Records that describe variables.

    """

    headings = (
        'Parameters',
        'Attributes',
        'Methods',
        'Returns',
        'Raises'
    )

    PRINTER_MD = printers.VarlistPrinterMD()
    PRINTER_RST = printers.VarlistPrinterRST()

    def __init__(self, heading, varrecords):
        self.heading = heading
        self.variables = varrecords


class VarRecord:
    """Object that describes a variable.

    Attributes
    ----------
    varname : str
        Variable name.
    vartype : str
        Variable type.
    vardoc : str
        Variable description.

    """

    def __init__(self, varname, vartype, vardoc):
        self.varname = varname
        self.vartype = vartype
        self.vardoc = vardoc

    def is_varrecord(self) -> True:
        return True
