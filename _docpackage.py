# -*- coding: utf-8 -*-
"""Create a report on a group of python scripts (package).

PKGPATH — Path to the package.
DOCPATH — Path where to place the output files.
"""

import docspyer

DOCPATH = '../_docs'
PKGPATH = '../docspyer/docmakers'

docspyer.cleardocs(DOCPATH)

docspyer.docpackage(
    PKGPATH, DOCPATH, mode='html', maxdepth=0
)
