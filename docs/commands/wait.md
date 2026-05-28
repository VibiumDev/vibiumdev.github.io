---
title: vibium wait
---

Block until something appears on the page.

## Synopsis

```
vibium wait "<selector>"
vibium wait url "<path>"
vibium wait text "<text>"
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
