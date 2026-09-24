---
title: vibium dblclick
---

Double-click an element.

## Synopsis

```
vibium dblclick [selector] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium dblclick "td.cell"
# Double-click to edit a table cell

vibium dblclick @e2
# Double-click element from map

vibium dblclick "td.cell" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
