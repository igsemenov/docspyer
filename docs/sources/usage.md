<!--
{
  "webtitle": "Usage — Docspy documentation",
  "codeblocks": true
}
-->

# Usage

## Inspect a script

Suppose you have a python script `myscript.py` located in some directory.

You can generate a report on this script as follows:

```python
import docspy

SCRIPTPATH = '../../myscript.py'  # Path to the python script.
DOCPATH = '../../mydocs'          # Path where to save the report.

# Generates a report in HTML.
# Use mode='md' to select the MD format.
docspy.docscript(
    SCRIPTPATH, DOCPATH, mode='html'
)
```

<b>Output in MD mode</b>

The report named `myscript.md` is generated in `mydocs`.

<b>Output in HTML mode</b>

The report named `myscript.html` and the necessary CSS/JS files are generated in `mydocs`:

```text
mydocs
├─ docpage.js
├─ docpage.css
└─ myscript.html
```

## Inspect a package

Suppose you have a directory with python scripts inside (package):

```text
mypackage
├─ alfa.py
└─ subpackage
   └─ bravo.py
```

You can create an overview of this package as follows:

```python
import docspy

DIRPATH = '../../mypackage' # Path to the package.
DOCPATH = '../../mydocs'    # Path where to save the report.

# Generates an overview in HTML.
# Use mode='md' to select the MD format.
docspy.docpackage(
    DIRPATH, DOCPATH, mode='html'
) 
```

<b>Output in MD mode</b>

The MD reports are generated in `mydocs`:

```text
mydocs
├─ mypackage.alfa.md
└─ mypackage.subpackage.bravo.md
```

<b>Output in HTML mode</b>

The HTML reports along with the necessary CSS/JS files are generated in `mydocs`:

```text
mydocs
├─ docpage.js
├─ docpage.css
├─ index.html
├─ mypackage.html
├─ subpackage.html
├─ mypackage.alfa.html
└─ mypackage.subpackage.bravo.html
```

Start `index.html` to explore the resulting overview. 