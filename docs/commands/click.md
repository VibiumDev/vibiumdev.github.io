---
title: vibium click
---

Click an element by reference.

## Synopsis

```
vibium click @e<num>
```

## Description

Performs a real mouse click on the element identified by `@e<num>`. The
reference must come from a recent [`map`](map.md) or [`find`](find.md) call.

Use [`wait`](wait.md) afterward if the click triggers navigation or a delayed
DOM update.

## Examples

Click the second mapped element:

```sh
vibium click @e2
```

Click an element you've located by text — find first, then click the
reference it returns:

```sh
$ vibium find text "Sign in"
@e4  link  "Sign in"

$ vibium click @e4
```

## See also

- [`vibium map`](map.md), [`vibium find`](find.md)
- [`vibium wait`](wait.md)
