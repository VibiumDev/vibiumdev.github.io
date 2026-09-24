---
title: vibium hover
---

Hover over an element by CSS selector.

## Synopsis

```
vibium hover [selector] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium hover "a"
# Hover over first link

vibium hover https://example.com "a"
# Navigate then hover

vibium hover "a" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
