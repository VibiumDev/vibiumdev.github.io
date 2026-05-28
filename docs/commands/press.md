---
title: vibium press
---

Send a keystroke to the focused element.

## Synopsis

```
vibium press <key>
```

## Description

Dispatches a real key event for `<key>`. Common values:

- Letters and digits: `a`, `B`, `7`
- Named keys: `Enter`, `Tab`, `Escape`, `Backspace`, `Delete`,
  `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight`, `Home`, `End`,
  `PageUp`, `PageDown`, `Space`

This is the simplest way to submit a form that responds to Enter, or to
navigate a custom keyboard-driven widget.

## Examples

Submit a search:

```sh
vibium fill @e3 "vibium"
vibium press Enter
```

Tab between fields:

```sh
vibium press Tab
```

## See also

- [`vibium fill`](fill.md) — type a whole string into an input.
