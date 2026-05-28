---
title: vibium find
---

Locate an element by a semantic attribute and return its reference.

## Synopsis

```
vibium find text "<text>"
vibium find label "<label>"
vibium find placeholder "<text>"
vibium find role <role>
```

## Description

`find` matches elements the way a human would describe them, returning one or
more `@eN` references you can pass to interaction commands.

| Variant                              | Matches                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------- |
| `vibium find text "<text>"`          | Elements whose visible text contains `<text>`.                          |
| `vibium find label "<label>"`        | Form fields whose `<label>` is `<label>`.                               |
| `vibium find placeholder "<text>"`   | Inputs with that placeholder.                                           |
| `vibium find role <role>`            | Elements with the given ARIA role (`button`, `searchbox`, `link`, …).   |

Each match is printed in the same form as [`vibium map`](map.md): a line per
element with its `@eN` reference, role, and a short description.

## Examples

```sh
vibium find text "Sign in"
vibium find label "Email"
vibium find placeholder "Search..."
vibium find role button
```

Typical workflow — find, then act on the reference:

```sh
$ vibium find label "Email"
@e2  input  label="Email"

$ vibium fill @e2 "alice@example.com"
```

## See also

- [`vibium map`](map.md) — list every element instead of finding one.
- [`vibium click`](click.md), [`vibium fill`](fill.md) — act on the result.
