---
title: vibium tap
sidebar:
  badge: Nightly
---

Tap a touchscreen at coordinates or on an element.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium tap [x] [y] | tap <selector|@ref> [flags]
```

## Examples

```sh
vibium tap 100 200
# Tap at (100, 200)

vibium tap @e1
# Tap the center of an element from find or map
```
