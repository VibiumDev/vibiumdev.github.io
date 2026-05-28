---
title: vibium pdf
---

Save the current page as a PDF.

## Synopsis

```
vibium pdf [-o <file>]
```

## Description

Renders the current page as a PDF document. With `-o`, writes to the given
file; without `-o`, writes to stdout.

Useful for archiving, sharing, or feeding the rendered document to a
PDF-aware downstream tool.

## Examples

```sh
vibium pdf -o page.pdf
vibium pdf > /tmp/page.pdf
```

## See also

- [`vibium screenshot`](screenshot.md) — image capture.
- [`vibium text`](text.md) — text-only capture.
