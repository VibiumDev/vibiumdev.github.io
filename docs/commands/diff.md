---
title: vibium diff map
---

Show how the page's interactive elements have changed since the last
[`map`](map.md).

## Synopsis

```
vibium diff map
```

## Description

After you run `vibium map`, Vibium remembers the snapshot of `@eN` references.
`vibium diff map` compares the current page against that snapshot and prints
only the differences:

- elements that appeared
- elements that disappeared
- elements whose description changed

This is the fast way to confirm that an interaction actually changed the page,
or to find a newly revealed widget (a modal, an autocomplete, an expanded
section) without re-reading the full map.

## Examples

```sh
vibium go https://example.com
vibium map
vibium click @e1
vibium diff map
```

## See also

- [`vibium map`](map.md)
- [`vibium wait`](wait.md)
