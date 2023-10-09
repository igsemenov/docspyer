# -*- coding: utf-8 -*-
"""Converts a numpy style docstring to MD.
"""

from . import parser


def docasmd(docstr) -> str:
    """Converts a numpy style docsrting to MD.

    Parameters
    ----------
    docstr : str
        Docstring to be converted.

    Returns
    -------
    str
        The resulting docstring in MD.

    """
    blocks = parse_doc_by_parser(docstr)
    return render_blocks_md(blocks)


def docasrst(docstr) -> str:
    """Converts a numpy style docsrting to RST.

    Parameters
    ----------
    docstr : str
        Docstring to be converted.

    Returns
    -------
    str
        The resulting docstring in RST.

    """
    blocks = parse_doc_by_parser(docstr)
    return render_blocks_rst(blocks)


def parse_doc_by_parser(docstr) -> list:
    return parser.parsedoc(docstr)


def render_blocks_md(blocks) -> str:
    return '\n\n'.join(
        [block.render_md() for block in blocks]
    )


def render_blocks_rst(blocks) -> str:
    return '\n\n'.join(
        [block.render_rst() for block in blocks]
    )
