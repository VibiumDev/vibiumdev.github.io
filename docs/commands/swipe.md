---
title: vibium swipe
sidebar:
  badge: Nightly
---

Swipe a touchscreen in a direction or from one point to another.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium swipe <up|down|left|right> | <x1> <y1> <x2> <y2> [flags]
```

## Flags

```
    --distance int   How far a direction swipe moves in pixels (default: half the viewport)
    --duration int   How long the move takes in milliseconds (default 300)
    --from string    Where a direction swipe starts: top, bottom, left, right, top-left, top-right, bottom-left, bottom-right, center, or x,y
    --hold int       Milliseconds to rest at the end before lifting
    --speed string   slow, normal, fast, or pixels per second (instead of --duration)
```

## Examples

```sh
vibium swipe up
# Swipe up from the viewport center, half the viewport height

vibium swipe left --distance 200
# Swipe left 200px from the center

vibium swipe up --from bottom --speed fast
# Phone (Roadie): go home

vibium swipe up --from bottom --speed slow --hold 500
# Phone (Roadie): open the app switcher

vibium swipe down --from top
# Phone (Roadie): Notification Center, or the Android notification shade

vibium swipe down --from top-right
# iPhone (Roadie): Control Center

vibium swipe up --from 200,600 --duration 600
# Swipe up from (200, 600) over 600ms

vibium swipe 200 400 200 100
# Swipe from (200, 400) to (200, 100)
```
