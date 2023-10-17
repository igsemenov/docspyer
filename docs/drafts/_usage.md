<!--
{{
  "webtitle": "Usage — docspyer documentation",
  "doctitle": "docspyer — Usage",
  "codeblocks": true
}}
-->

# Generate reports

`docspyer` can create reports on:

- A single python script.
- A group of python scripts (package).

## Inspect a script

Example of creating a report on a script:

```python
{_docscript-py}
```

For more information see {*#docspyer-docscript*}

## Inspect a package

Example of creating a report on a package:

```python
{_docpackage-py}
```

For more information see {*#docspyer-docpackage*}

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
- Consider using {*#docspyer-DocFormat*} when preparing source files.

### Metadata 

A source file <em>may</em> contain a header with JSON metadata:

```text
{docspyer-docmakers-docbuilder-SourceFile-META_EXAMPLE}
```

<i>Remarks</i>

- The header must be a first paragraph of the source file.
- JSON data overwrites the default settings of the HTML page builder.

### Index file

The root file — `index.md` — is mandatory.

This file <em>must</em> contain the documentation outline (global TOC):

```text
{docspyer-docmakers-docbuilder-IndexFile-TOC_EXAMPLE}
```

<i>Specification</i>

- Heading title — `Contents` — is mandatory.
- Heading level is flexible (1, 2, ...).
- Links format (MD) is mandatory.

### Modules

Consider using {#docspyer-docmods} to document modules dynamically (as live objects).

## Run the builder

For more information see {#docspyer-builddocs}.

Example of building a documentation:

```python
{_makedocs-py}
```
