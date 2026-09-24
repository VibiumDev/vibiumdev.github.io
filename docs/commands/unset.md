---
title: vibium unset
sidebar:
  badge: Nightly
---

Uncheck a checkbox.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

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
