# -*- coding: utf-8 -*-
"""Test the parser of MD text.
"""

import unittest
from docspyer.docpage.textmd import parser

mdparser = parser.MDParser()
parsetext = parser.parsetext
find_type = parser.ParTypeFinder().find_type

TEXT_HEADINGS = """
# Alfa

## Bravo

### Charlie
"""

TEXT_CODEBLOCK = """
```
Alfa

Bravo

Charlie
```
"""

TEXT_CODEBLOCK_FIXED = """
``````
```Alfa
```
```Bravo
```
```Charlie
``````
"""

TEXT_LIST = """
- Alfa
- Bravo
"""

TEXT_TABLE = """
Name  | Description
----  | -----------
Alfa  | First item
Bravo | Second item
"""

TEXT_HTML_TAG = """
<tag>
</tag>
"""


# Strip constants.
for key, val in list(globals().items()):
    if isinstance(val, str):
        if key.isupper():
            globals()[key] = val.strip()


class TestParser(unittest.TestCase):

    def test_fixcodeblocks(self):
        res_of_fixcodeblocks = mdparser.fixcodeblocks(TEXT_CODEBLOCK)
        assert res_of_fixcodeblocks == TEXT_CODEBLOCK_FIXED

    def test_headings(self):

        res = parsetext(TEXT_HEADINGS)

        block_heading_1, block_heading_2, block_heading_3 = res

        assert block_heading_1.text == '# Alfa'
        assert block_heading_2.text == '## Bravo'
        assert block_heading_3.text == '### Charlie'

    def test_code_block(self):
        block_code, = parsetext(TEXT_CODEBLOCK)
        assert block_code.text == TEXT_CODEBLOCK

    def test_list(self):
        block_list, = parsetext(TEXT_LIST)
        assert block_list.text == TEXT_LIST

    def test_one_column_table(self):
        block_table, = parsetext(TEXT_TABLE)
        assert block_table.text == TEXT_TABLE


class TestTypeFinder(unittest.TestCase):

    def test_is_hrule(self):
        assert find_type('---') == 'hrule'
        assert find_type('===') == 'hrule'
        assert find_type('***') == 'hrule'

    def test_heading(self):
        assert find_type('# Alfa') == 'heading'
        assert find_type('## Bravo') == 'heading'
        assert find_type('### Charlie') == 'heading'

    def test_is_list(self):
        assert find_type(TEXT_LIST) == 'list'

    def test_is_code(self):
        assert find_type(TEXT_CODEBLOCK) == 'code'

    def test_is_table(self):
        assert find_type(TEXT_TABLE) == 'table'

    def test_html_blocks_are_pars(self):
        assert find_type(TEXT_HTML_TAG) == 'par'


if __name__ == '__main__':
    unittest.main()
