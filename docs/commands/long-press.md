---
title: vibium long-press
sidebar:
  badge: Nightly
---

Press and hold a touchscreen at coordinates.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

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
