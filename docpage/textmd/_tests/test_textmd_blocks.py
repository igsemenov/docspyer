# -*- coding: utf-8 -*-
"""Test blocks of MD text.
"""

import unittest
from docspyer.docpage.textmd import blocks

HEADING = '# Alfa'

HEADING_HTML = """
<div class="toc-anchor"></div><h1>Alfa</h1>
"""

LIST_MD = """
- Alfa
- Bravo
"""

LIST_HTML = """
<p>
<ul class="md-list">
    <li>Alfa</li>
    <li>Bravo</li>
</ul>
</p>
"""


TABLE = """
Name  | Description
----  | -----------
Alfa  | First item
Bravo | Second item
"""

TABLE_HTML = """
<table>
    <tr>
        <th>Name</th>
        <th>Description</th>
    </tr>
    <tr>
        <td>Alfa</td>
        <td>First item</td>
    </tr>
    <tr>
        <td>Bravo</td>
        <td>Second item</td>
    </tr>
</table>
"""

TEXT_BLOCK = """
```
Alfa

Bravo
```
"""

TEXT_BLOCK_HTML = """
<pre class="docstring">Alfa

Bravo</pre>
"""

PYTHON_BLOCK = """
```python
Alfa

Bravo
```
"""

LANGLABEL = """<span class="lang-name">Python</span>"""

PYTHON_BLOCK_HTML = f"""
<pre>{LANGLABEL}<code class="language-python">Alfa

Bravo</code></pre>
"""


# Strip constants.
for key, val in list(globals().items()):
    if isinstance(val, str):
        if key.isupper():
            globals()[key] = val.strip()


class TestMDBlocks(unittest.TestCase):

    def test_heading(self):
        block = blocks.MDHeading(HEADING)
        assert block.make_html() == HEADING_HTML

    def test_table(self):
        block = blocks.MDTable(TABLE)
        assert block.make_html() == TABLE_HTML

    def test_list(self):
        block = blocks.MDList(LIST_MD)
        assert block.make_html() == LIST_HTML

    def test_text_block(self):

        block = blocks.MDCode(TEXT_BLOCK)
        lang, body = block.parse_block()

        assert lang == ''
        assert body == 'Alfa\n\nBravo'
        assert block.make_html() == TEXT_BLOCK_HTML

    def test_python_block(self):

        block = blocks.MDCode(PYTHON_BLOCK)
        lang, body = block.parse_block()

        assert lang == 'python'
        assert body == 'Alfa\n\nBravo'
        assert block.make_html() == PYTHON_BLOCK_HTML


if __name__ == '__main__':
    unittest.main()
