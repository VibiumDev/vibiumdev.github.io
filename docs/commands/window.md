---
title: vibium window
---

Get or set the OS browser window size, position, or state.

## Synopsis

```
vibium window [width] [height] [x] [y] [flags]
```

## Flags

```
    --state string   Window state: normal, maximized, minimized, fullscreen
```

## Examples

```sh
vibium window
# {"state":"normal","x":0,"y":25,"width":1280,"height":720}

vibium window 1920 1080
# Set window to 1920x1080

vibium window 1920 1080 0 0
# Set window to 1920x1080 at position (0, 0)

vibium window --state maximized
# Maximize the window
```
