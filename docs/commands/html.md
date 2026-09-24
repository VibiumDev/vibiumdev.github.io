---
title: vibium html
---

Get HTML content of the page or an element.

## Synopsis

```
vibium html [selector] [flags]
```

## Flags

```
    --outer   Return outerHTML instead of innerHTML
```

## Examples

```sh
vibium html
# Get full page HTML

vibium html "div.content"
# Get innerHTML of a specific element

vibium html "div.content" --outer
# Get outerHTML of a specific element

vibium html https://example.com "h1"
# Navigate then get element HTML
```
