---
title: vibium fill
---

Type text into an input field.

## Synopsis

```
vibium fill @e<num> "<value>"
```

## Description

Focuses the element referenced by `@e<num>` and types `<value>` into it. Works
for any input that accepts text: `<input type="text">`, `<input type="email">`,
`<input type="password">`, `<textarea>`, `contenteditable` elements, and so on.

## Examples

```sh
vibium fill @e2 "alice@example.com"
vibium fill @e3 "correct horse battery staple"
```

When you don't know the reference yet, find it first:

```sh
$ vibium find label "Email"
@e2  input  label="Email"

$ vibium fill @e2 "alice@example.com"
```

## See also

- [`vibium press`](press.md) — send a single keystroke (e.g. `Enter`).
- [`vibium select`](select.md), [`vibium check`](check.md).
