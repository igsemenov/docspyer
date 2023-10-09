<!--
{
  "webtitle": "Docspy documentation",
  "codeblocks": true
}
-->

## Contents

- [Usage](usage.md)
- [Modules](modules.md)
  - [docspy](docspy.md)
  - [docspy.inspect](docspy.inspect.md)

## Overview

### Installation

The package is small enough to be used without pre-installation.

Download the package and add it to `sys.path`:

```python
import sys

PATH_TO_PACKAGE = '../../dir-with-package-inside'

if PATH_TO_PACKAGE not in sys.path:
  sys.path.append(PATH_TO_PACKAGE)
```

After that import the package as usual:

```python
import docspy
```