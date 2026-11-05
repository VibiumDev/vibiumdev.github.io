---
title: vibium type
---

Type text into an element, or into whatever has focus.

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
vibium type "calc"
# Types into whatever has focus: a search box, or a phone's screen

vibium type "input" "12345"
# Types into the element on the current page

vibium type https://the-internet.herokuapp.com/inputs "input" "12345"
# Navigates to URL first, then types

vibium type https://the-internet.herokuapp.com/inputs "input" "12345" --timeout 5s
# Custom timeout (5s, or 5000 for milliseconds)
```
