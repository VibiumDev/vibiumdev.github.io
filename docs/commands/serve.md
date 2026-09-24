---
title: vibium serve
---

Start WebSocket proxy server for browser automation.

## Synopsis

```
vibium serve [flags]
```

## Flags

```
-p, --port int   Port to listen on (default 9515)
```

## Examples

```sh
vibium serve
# Starts server on default port 9515, visible browser

vibium serve --port 8080
# Starts server on port 8080

vibium serve --headless
# Starts server with headless browser
```
