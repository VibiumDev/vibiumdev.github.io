---
title: vibium unset
---

Uncheck a checkbox.

## Synopsis

```
vibium unset [selector] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium unset "input[name=agree]"
# Uncheck the "agree" checkbox (idempotent)

vibium unset "input[name=agree]" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
