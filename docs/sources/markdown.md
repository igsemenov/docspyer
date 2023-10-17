<!--
{
  "webtitle": "Markdown — docspyer documentation",
  "doctitle": "docspyer — Markdown",
  "codeblocks": false
}
-->

# Overview

MD text is considered as a sequence of blocks.

**Block types**

- [Heading](#heading)
- [Rule](#rule)
- [Par](#par)
- [List](#list)
- [Table](#table)
- [Code](#code)

**Block structure**

- All blocks except code blocks are single paragraphs.
- A code block may contain several paragraphs.

# Blocks

## Heading

<i>Example</i>

```text
# Heading
```

<i>Specification</i>

- Occupies a single line.
- Must start with `#{1,}\s`.

## Rule

<i>Specification</i>

- Represents a horizontal line.
- Matches the regexp `[-=\*]{3,}`.

## Par

<i>Example</i>

```text
Some ordinary paragraph that is 
not a heading, list, table, ...
```

<i>Specification</i>

- Represents an ordinary piece of text.
- Dumped to HTML as it is, when is an <i>HTML block</i>.

<i>HTML blocks</i>

Paragraphs starting with `<(p|dl|div|svg)` or HTML comments.

## List

<i>Example</i>

```text
- Alfa
- Bravo
  - Charlie
    Delta
    - Echo
```

<i>Specification</i>

- Must start with the iterator `-\s`.
- Multiline items are allowed, see `Charlie...` item.

## Table

<i>Example</i>

```text
Name  | Info
------|--------
Alfa  | Bravo
Delta | Charlie
```

<i>Specification</i>

- Follows the <i>one-line-is-one-row</i> structure.
- Columns are separated by `|`.
- The first row is a table head.

## Code

<i>Specification</i>

- May contain several paragraphs.
- Must start and end with three backticks.
- Code language — `LANG` — is fetched from the first line.

Code blocks can represent

- Code snippets.
- Text snippets.

<i>Code snippets</i>

- Dumped to HTML as `&lt;pre>&lt;code>` pair.
- CSS class `language-LANG` is assigned to `&lt;code>`.
- `LANG` can be `python|c`.

<i>Text snippets</i>

- Dumped to HTML as `&lt;pre>` tag.
- Assigned CSS class is `LANG`.
