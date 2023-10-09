# -*- coding: utf-8 -*-
"""Creates the `docspyer` documentation.
"""

import docspyer

SRCPATH = 'docs/sources'
DOCPATH = 'docs/build'

LOGO = docspyer.docpage.pagemaker.getlogo()
LOGO += '<p id="logo-title">docspyer</p>'

MODULES = [
    docspyer
]

docspyer.docmods(MODULES, SRCPATH)

config = {
    'doclogo': LOGO,
    'swaplinks': True,
    'codeblocks': True,
    'extracss': '_theme.css'
}

docspyer.builddocs(SRCPATH, DOCPATH, **config)
