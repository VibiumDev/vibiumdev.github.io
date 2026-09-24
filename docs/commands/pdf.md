---
title: vibium pdf
---

Save page as PDF.

## Synopsis

```
vibium pdf [url] [flags]
```

## Flags

```
    --background           Print background graphics
    --landscape            Landscape orientation
    --margin float         Margin on all sides in cm (default 1)
-o, --output string        Output file path (default "page.pdf")
    --page-height float    Page height in cm (default 27.94)
    --page-ranges string   Pages to print, e.g. 1,3-5 (default all)
    --page-width float     Page width in cm (default 21.59)
    --scale float          Print scale, 0.1-2 (default 1)
```

New in nightly (not yet in the npm release): `--background`, `--landscape`, `--margin`, `--page-height`, `--page-ranges`, `--page-width`, `--scale`

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
