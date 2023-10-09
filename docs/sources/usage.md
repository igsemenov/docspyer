<!--
{
  "webtitle": "Usage — docspyer documentation",
  "doctitle": "docspyer — Usage",
  "codeblocks": true
}
-->

# Generate reports

`docspyer` can create reports on:

- A single python script.
- A group of python scripts (package).

## Inspect a script

Example of creating a report on a script:

```python
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

```

For more information see [docspyer.docscript()](docspyer.md#docscript)

## Inspect a package

Example of creating a report on a package:

```python
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

```

For more information see [docspyer.docpackage()](docspyer.md#docpackage)

# Build documentation

`docspyer` can build HTML documentation from MD source files.

## Source files

Collect source files in a separate folder, for example:

```text
../docs/sources
 ├─ index.md
 ├─ ...
 └─ *.md
```

### Format

- Source files should be prepared using the [Markdown](appendix.md) format.
- Consider using [docspyer.DocFormat](docspyer.md#docformat) when preparing source files.

### Metadata 

A source file <em>may</em> contain a header with JSON metadata:

```text

<!--
{
  "webtitle": "WEBTITLE",
  "doctitle": "DOCTITLE",
  "codeblocks": true/false
}
-->

```

<i>Remarks</i>

- The header must be a first paragraph of the source file.
- JSON data overwrites the default settings of the HTML page builder.

### Index file

The root file — `index.md` — is mandatory.

This file <em>must</em> contain the documentation outline (global TOC):

```text

## Contents

- [Section](*.md)
  - [Subsection](*.md)

```

<i>Specification</i>

- Heading title — `Contents` — is mandatory.
- Heading level is flexible (1, 2, ...).
- Links format (MD) is mandatory.

### Modules

Consider using [docspyer.docmods()](docspyer.md#docmods) to document modules dynamically (as live objects).

## Run the builder

For more information see [docspyer.builddocs()](docspyer.md#builddocs).

Example of building a documentation:

```python
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

```
