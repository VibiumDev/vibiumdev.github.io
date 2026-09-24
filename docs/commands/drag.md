---
title: vibium drag
---

Drag from one element to another.

## Synopsis

```
vibium drag [source] [target] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium drag ".draggable" ".dropzone"
# Drag element to drop target

vibium drag @e1 @e3
# Drag using map refs

vibium drag ".draggable" ".dropzone" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
