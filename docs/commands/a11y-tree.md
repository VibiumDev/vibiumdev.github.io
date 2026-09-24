---
title: vibium a11y-tree
---

Get the accessibility tree of the current page.

## Synopsis

```
vibium a11y-tree [flags]
```

## Flags

```
    --everything   Show all nodes including generic containers
```

## Examples

```sh
vibium a11y-tree
# Print the accessibility tree (interesting nodes only)

vibium a11y-tree --everything
# Include all nodes (generic containers, etc.)
```
