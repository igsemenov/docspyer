# -*- coding: utf-8 -*-
"""Script that creates the package documentation.
"""

import docspy

SRCPATH = 'docs/sources'
DOCPATH = 'docs/build'

LOGO = docspy.docpage.pagemaker.getlogo()
LOGO += '<p id="logo-title">Docspy</p>'

LOGOCSS = """
#logo-title {
  opacity: 0.9;
  font-size: 22px;
  font-weight: bold;
  padding-left: 12px;
  color: var(--black-color);s
}
"""

MODULES = [
    docspy, docspy.inspect
]

docspy.docmodules(
    MODULES, SRCPATH, hostname='Docspy'
)

config = {
    'doclogo': LOGO,
    'codeblocks': True,
    'swaplinks': True,
    'extracss': LOGOCSS.strip()
}

docspy.builddocs(SRCPATH, DOCPATH, config)
