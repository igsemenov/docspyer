# -*- coding: utf-8 -*-
"""Formats drafts of the source files.
"""

import docspyer
from docspyer.docmakers import formatdoc

DRAFTS = [
    '_usage.md',
    '_appendix.md',
    '_markdown.md'
]

SRCDIRS = [
    '../../',
    '../drafts',
    '../sources'
]

formatter = formatdoc.DocFormat()
formatter.setconfig(SRCDIRS, hostmod=docspyer)

for name in DRAFTS:

    dstname = name.removesuffix('.md').lstrip('_')

    formatter.formatdoc(
        srcpath=name, dstpath=f'../sources/{dstname}.md'
    )
