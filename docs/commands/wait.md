---
title: vibium wait
---

Wait for an element, URL, text, page load, or JS condition.

## Synopsis

```
vibium wait [selector] [flags]
vibium wait [command]
```

## Flags

```
    --state string      State to wait for: attached, visible, hidden (default "attached")
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Subcommands

### vibium wait fn

Wait until a JS expression returns truthy.

```
vibium wait fn [expression] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium wait fn "document.readyState === 'complete'"
# Wait for page to be fully loaded

vibium wait fn "window.ready === true" --timeout 10s
# Wait for custom condition (10s, or 10000 for milliseconds)
```

### vibium wait load

Wait until the page is fully loaded.

```
vibium wait load [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium wait load
# Wait until document.readyState is "complete"

vibium wait load --timeout 10s
# Wait up to 10 seconds (or 10000 for milliseconds)
```

### vibium wait text

Wait until text appears on the page.

```
vibium wait text [text] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium wait text "Welcome"
# Waits until "Welcome" appears on the page

vibium wait text "Success" --timeout 10s
# Wait with custom timeout (10s, or 10000 for milliseconds)
```

### vibium wait url

Wait until the page URL contains a substring.

```
vibium wait url [pattern] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium wait url "/dashboard"
# Wait until URL contains "/dashboard"

vibium wait url "success" --timeout 10s
# Wait up to 10 seconds (or 10000 for milliseconds)
```

## Description

`wait` is how you synchronize with asynchronous browser behavior — navigation,
network responses, animation, dynamic re-renders. It blocks until its
condition becomes true, then exits successfully. If the condition never
becomes true within Vibium's wait timeout, the command exits with an error.

| Variant                          | Becomes true when…                                |
| -------------------------------- | ------------------------------------------------- |
| `vibium wait "<selector>"`       | An element matching `<selector>` is on the page.  |
| `vibium wait url "<path>"`       | The current URL contains `<path>`.                |
| `vibium wait text "<text>"`      | `<text>` appears anywhere in the visible page.    |

## Examples

Wait for a button to appear:

```sh
vibium wait "button.continue"
```

Wait for a path change:

```sh
vibium wait url "/results"
```

Wait for a result to be rendered:

```sh
vibium wait text "Results for"
```

## See also

- [`vibium go`](go.md), [`vibium click`](click.md) — actions that often
  warrant a `wait` afterward.
- [`vibium diff map`](diff.md) — alternative way to confirm a change.
