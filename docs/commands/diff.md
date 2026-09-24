---
title: vibium diff
---

Compare current state vs previous.

## Synopsis

```
vibium diff [flags]
vibium diff [command]
```

## Subcommands

### vibium diff map

Compare current page elements vs last map.

```
vibium diff map [flags]
```

```sh
vibium map           # take initial snapshot
vibium click @e3     # interact with page
vibium diff map      # see what changed
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
