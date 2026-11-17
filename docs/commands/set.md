---
title: vibium set
---

Check a checkbox or radio button.

## Synopsis

```
vibium set [selector] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium set "input[name=agree]"
# Check the "agree" checkbox (idempotent)

vibium set "input[name=agree]" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
