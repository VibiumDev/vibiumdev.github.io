---
title: vibium map
---

List the interactive elements on the current page as numbered references.

## Synopsis

```
vibium map
```

## Description

Scans the current page for interactive elements (links, buttons, inputs,
selects, checkboxes, role-based widgets) and prints each one with a stable
reference of the form `@eN`. You then pass those references to interaction
commands like [`click`](click.md), [`fill`](fill.md), or [`select`](select.md).

References are stable for the lifetime of the page. When the DOM changes
(navigation, dynamic re-render, etc.), call `map` again — or use
[`diff map`](diff.md) to see only what changed.

## Output

Each line contains:

- The reference (`@e1`, `@e2`, …)
- The element role (`link`, `button`, `input`, `select`, …)
- A short human-readable description (visible text, label, placeholder, etc.)

Example:

```
@e1  link    "Sign in"
@e2  input   placeholder="Email"
@e3  input   placeholder="Password"
@e4  button  "Continue"
```

## Examples

```sh
vibium go https://example.com
vibium map
```

## See also

- [`vibium diff map`](diff.md)
- [`vibium find`](find.md)
- [`vibium screenshot`](screenshot.md)
