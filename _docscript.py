# -*- coding: utf-8 -*-
"""Create a report on a python script.

SRCPATH — Path to the the script.
DOCPATH — Path where to place the output files.
"""

import docspyer

DOCPATH = '../_docs'
SRCPATH = 'docmakers/docmods.py'

docspyer.cleardocs(DOCPATH)

docspyer.docscript(
    SRCPATH, DOCPATH, mode='html'
)
