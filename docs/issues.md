# Issues

## Issue-01

- Problem in `builddocs()` with HTML rendering of `Contents` in `index.md`.
- Wrong handling of trailing spaces after a TOC entry — `[Section](*.md)`
- Broken HTML link is generated.

## Issue-02

- Problem when rendering MD tables in HTML.
- Living empty cells in a column leads to a column collapse.

This table

```
Term | Description
-----|------------
A    | About A
B    | 
```

will not have `Description` in HTML.