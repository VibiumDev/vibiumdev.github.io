---
title: vibium eval
---

Run JavaScript in the current page.

## Synopsis

```
vibium eval "<javascript>"
```

## Description

Executes `<javascript>` in the page context and prints the result to stdout.
The script has full access to `window`, `document`, and any globals the page
exposes.

This is the escape hatch for anything Vibium's higher-level commands don't
cover — extracting computed values, dispatching custom events, querying the
DOM with a custom selector, and so on. Reach for `eval` when the semantic
commands aren't enough; reach for the semantic commands first.

## Examples

```sh
vibium eval "document.title"
vibium eval "document.querySelectorAll('article').length"
vibium eval "window.scrollTo(0, document.body.scrollHeight)"
```

## See also

- [`vibium text`](text.md), [`vibium find`](find.md) — prefer these when they fit.
