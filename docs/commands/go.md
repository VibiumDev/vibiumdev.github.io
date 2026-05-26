---
title: vibium go
---

Navigate the active tab to a URL.

## Synopsis

```
vibium go <url>
```

## Description

Loads `<url>` in the current page. If no browser is running, Vibium starts one
first; otherwise it reuses the existing session.

The command returns once the navigation has committed. To wait for specific
content to be ready, follow up with [`vibium wait`](wait.md).

## Examples

```sh
vibium go https://example.com
vibium go https://github.com/VibiumDev/vibium
```

## See also

- [`vibium wait`](wait.md) — block on a URL change or element appearance.
- [`vibium map`](map.md) — list elements on the new page.
