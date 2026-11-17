---
title: vibium long-press
---

Press and hold a touchscreen at coordinates.

## Synopsis

```
vibium long-press [x] [y] [flags]
```

## Flags

```
    --duration int   How long to hold the press in milliseconds (default 500)
```

## Examples

```sh
vibium long-press 100 200
# Hold a press at (100, 200) for 500ms

vibium long-press 100 200 --duration 1200
# Hold for 1200ms
```
