---
title: vibium focus
---

Focus an element.

## Synopsis

```
vibium focus [selector] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium focus "input[name=email]"
# Focus the email input

vibium focus @e1
# Focus element from map

vibium focus "input[name=email]" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
