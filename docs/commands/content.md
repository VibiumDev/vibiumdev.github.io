---
title: vibium content
---

Replace the page HTML content.

## Synopsis

```
vibium content [html] [flags]
```

## Flags

```
    --stdin   Read HTML from stdin
```

## Examples

```sh
vibium content "<h1>Hello World</h1>"
# Set page content directly

echo "<h1>Hello</h1>" | vibium content --stdin
# Set page content from stdin
```
