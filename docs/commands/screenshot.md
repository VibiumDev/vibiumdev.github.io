---
title: vibium screenshot
---

Capture a screenshot (optionally navigate to URL first).

## Synopsis

```
vibium screenshot [url] [flags]
```

## Flags

```
    --annotate        Annotate interactive elements with numbered labels
    --full-page       Capture the full page instead of just the viewport
-o, --output string   Output file path (default "screenshot.png")
```

## Description

Saves a PNG of the visible page. With `-o`, the file is written to the given
path; without `-o`, the image is written to stdout (so you can pipe it into
`base64`, `feh -`, or another tool).

## Examples

```sh
vibium screenshot -o homepage.png
vibium screenshot > /tmp/page.png
```

## See also

- [`vibium pdf`](pdf.md) — save the whole document as PDF instead.
- [`vibium map`](map.md) — list the same `@eN` references textually.
