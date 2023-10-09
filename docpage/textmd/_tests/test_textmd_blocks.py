# -*- coding: utf-8 -*-
"""Test blocks of MD text.
"""

import unittest
from docspy.docpage.textmd import blocks

HEADING = '# Alfa'

HEADING_HTML = """
<div class="toc-anchor"></div><h1>Alfa</h1>
"""

PLAIN_LIST = """
- Alfa
- Bravo
"""

PLAIN_LIST_HTML = """
<p>
<ul>
    <li>Alfa</li>
    <li>Bravo</li>
</ul>
</p>
"""

LIST_WITH_NESTED_ITEM = """
- Alfa
  - Bravo
- Charlie
"""

LIST_WITH_NESTED_ITEM_HTML = """
<p>
<ul>
    <li>Alfa
        <ul>
            <li>Bravo</li>
        </ul>
    </li>
    <li>Charlie</li>
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
<pre>Alfa

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
        block_heading = blocks.MDHeading(HEADING)
        assert block_heading.make_html() == HEADING_HTML

    def test_table(self):
        block_table = blocks.MDTable(TABLE)
        assert block_table.make_html() == TABLE_HTML

    def test_plain_list(self):
        block_list = blocks.MDList(PLAIN_LIST)
        assert block_list.make_html() == PLAIN_LIST_HTML

    def test_list_with_nested_item(self):
        block_list = blocks.MDList(LIST_WITH_NESTED_ITEM)
        assert block_list.make_html() == LIST_WITH_NESTED_ITEM_HTML

    def test_text_block(self):
        block_code = blocks.MDCode(TEXT_BLOCK)
        assert block_code.make_html() == TEXT_BLOCK_HTML

    def test_python_block(self):
        block_code = blocks.MDCode(PYTHON_BLOCK)
        assert block_code.make_html() == PYTHON_BLOCK_HTML

    def test_code_get_content(self):
        block_code = blocks.MDCode(TEXT_BLOCK)
        assert block_code.get_content_from_body() == 'Alfa\n\nBravo'


if __name__ == '__main__':
    unittest.main()
