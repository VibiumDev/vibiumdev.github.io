---
title: vibium type
---

Type text into an element (optionally navigate to URL first).

## Synopsis

```
vibium type [url] [selector] [text] [flags]
```

## Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Examples

```sh
vibium type "input" "12345"
# Types on current page

vibium type https://the-internet.herokuapp.com/inputs "input" "12345"
# Navigates to URL first, then types

vibium type https://the-internet.herokuapp.com/inputs "input" "12345" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
