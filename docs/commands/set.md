---
title: vibium set
sidebar:
  badge: Nightly
---

Check a checkbox or radio button.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

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
