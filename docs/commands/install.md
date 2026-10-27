---
title: vibium install
---

Download the selected browser (Chrome for Testing by default).

## Synopsis

```
vibium install [flags]
```

## Examples

```sh
vibium install
# Downloads Chrome for Testing, at the version this vibium pins

vibium install --engine firefox
# Downloads Firefox, at the version this vibium pins

vibium install --engine firefox --channel beta
# Downloads the current Firefox beta
```
