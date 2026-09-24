---
title: vibium upload
---

Set files on an input[type=file] element.

## Synopsis

```
vibium upload [selector] [files...] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium upload "input[type=file]" ./photo.jpg
# Upload a single file

vibium upload "#file-input" ./photo.jpg ./doc.pdf
# Upload multiple files

vibium upload "input[type=file]" ./photo.jpg --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
