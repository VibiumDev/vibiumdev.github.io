---
title: vibium scroll
---

Scroll the page or an element.

## Synopsis

```
vibium scroll [up|down|left|right] [flags]
vibium scroll [command]
```

## Flags

```
    --amount int        Number of scroll increments (default 3)
    --selector string   CSS selector for the element to scroll within
```

## Subcommands

### vibium scroll into-view

Scroll an element into view.

```
vibium scroll into-view [selector] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium scroll into-view "#footer"
# Scroll the footer element into view (centered on screen)

vibium scroll into-view "#footer" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```

## Examples

```sh
vibium scroll
# Scroll down by default

vibium scroll up
# Scroll up

vibium scroll right --amount 5
# Scroll right 5 increments

vibium scroll down --selector "div.content"
# Scroll within a specific element
```
