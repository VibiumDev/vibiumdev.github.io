---
title: vibium check
---

Toggle a checkbox.

## Synopsis

```
vibium check @e<num>
```

## Description

Sets the checkbox referenced by `@e<num>` to its checked state. If you need to
explicitly uncheck a checked box, click it directly with [`click`](click.md)
instead.

## Examples

```sh
vibium check @e7
```

Find first, then check:

```sh
$ vibium find label "I agree to the terms"
@e7  input  label="I agree to the terms"

$ vibium check @e7
```

## See also

- [`vibium click`](click.md), [`vibium select`](select.md), [`vibium fill`](fill.md).
