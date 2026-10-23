---
title: vibium swipe
sidebar:
  badge: Nightly
---

Swipe a touchscreen from one point to another.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium swipe [x1] [y1] [x2] [y2] [flags]
```

## Flags

```
    --duration int   How long the move takes in milliseconds (default 300)
```

## Examples

```sh
vibium swipe 200 400 200 100
# Swipe up from (200, 400) to (200, 100)

vibium swipe 50 300 350 300 --duration 600
# Slower swipe right, over 600ms
```
