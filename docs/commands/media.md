---
title: vibium media
---

Override CSS media features.

## Synopsis

```
vibium media [flags]
```

## Flags

```
    --color-scheme string     Color scheme: light, dark, no-preference
    --contrast string         Contrast: more, less, no-preference
    --forced-colors string    Forced colors: active, none
    --media string            Media type: screen, print
    --reduced-motion string   Reduced motion: reduce, no-preference
```

## Examples

```sh
vibium media --color-scheme dark
# Enable dark mode

vibium media --reduced-motion reduce
# Reduce motion

vibium media --color-scheme light --forced-colors active
# Override multiple features
```
