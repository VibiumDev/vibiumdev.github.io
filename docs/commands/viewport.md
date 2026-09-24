---
title: vibium viewport
---

Get or set the browser viewport size.

## Synopsis

```
vibium viewport [width] [height] [flags]
```

## Flags

```
    --dpr float   Device pixel ratio (e.g., 2 for Retina)
```

## Examples

```sh
vibium viewport
# {"width":1280,"height":720,"devicePixelRatio":1}

vibium viewport 1280 720
# Set viewport to 1280x720

vibium viewport 375 812 --dpr 3
# Simulate iPhone X viewport
```
