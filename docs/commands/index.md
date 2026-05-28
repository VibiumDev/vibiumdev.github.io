---
title: Overview
sidebar:
  order: 0
---

The Vibium CLI commands you'll reach for in day-to-day use, grouped by
purpose. Each entry has its own page with syntax, flags, and examples.

> **Scope.** This reference covers the commands needed to drive the
> quickstart, the tutorial, and the typical agent loop. The `vibium`
> binary exposes additional lower-level commands (run `vibium --help`
> to list them) — they're useful escape hatches but are not part of the
> documented surface yet.

## Navigation

- [`vibium go`](go.md) — navigate to a URL.

## Mapping & references

- [`vibium map`](map.md) — list interactive elements as `@eN` references.
- [`vibium diff map`](diff.md) — show how the page has changed since the last map.

## Finding elements

- [`vibium find`](find.md) — locate elements semantically by text, label,
  placeholder, or ARIA role.

## Interacting

- [`vibium click`](click.md) — click an element by reference.
- [`vibium fill`](fill.md) — type text into an input.
- [`vibium select`](select.md) — choose a dropdown option.
- [`vibium check`](check.md) — toggle a checkbox.
- [`vibium press`](press.md) — send a keystroke.

## Waiting

- [`vibium wait`](wait.md) — block until an element, URL, or text appears.

## Capture

- [`vibium text`](text.md) — extract page text.
- [`vibium screenshot`](screenshot.md) — save a PNG screenshot.
- [`vibium pdf`](pdf.md) — save the page as a PDF.
- [`vibium eval`](eval.md) — run JavaScript in the page.

## Recording

- [`vibium record`](record.md) — start/stop a session recording.

## Agent integration

- [`vibium mcp`](mcp.md) — start the MCP server.

## Conventions

- Arguments shown as `<x>` are required; `[x]` are optional.
- `@eN` always refers to a numeric element reference returned by `map` or `find`.
- All commands share a single browser/daemon, so state persists across calls.
- Output is plain text on stdout unless a `-o` flag specifies a file.

## Running without installing

Every command on every page below also works through `npx` — no global
install required:

```sh
npx -y vibium go https://example.com
npx -y vibium map
npx -y vibium screenshot -o page.png
```

For a session-wide alias:

```sh
alias vibium='npx -y vibium'
```
