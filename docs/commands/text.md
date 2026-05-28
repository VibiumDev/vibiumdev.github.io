---
title: vibium text
---

Extract the visible text of the current page.

## Synopsis

```
vibium text
```

## Description

Prints the rendered, human-visible text content of the page to stdout. This is
the cleanest way to give an agent the "what does the user see" view of the
page without HTML noise.

The output is plain text suitable for `grep`, redirection, or piping into
another tool.

## Examples

```sh
vibium text
vibium text > page.txt
vibium text | grep -i "error"
```

## See also

- [`vibium screenshot`](screenshot.md) — visual capture instead of textual.
- [`vibium eval`](eval.md) — run JavaScript to extract a more specific value.
