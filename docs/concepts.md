---
title: Core Concepts
---

A short tour of the ideas that make Vibium feel different from older browser
automation tools.

## The browser daemon

Vibium runs a long-lived daemon that owns the browser process. Each `vibium`
command is a small client that talks to that daemon over a local socket. Two
practical consequences:

- Commands are **fast** — there is no per-command startup cost.
- State **persists** between commands — cookies, the current page, the active
  tab, scroll position, and element references all carry over.

The daemon shuts down on demand, when you explicitly stop it, or when the
session ends.

From a script using a client library, always pair `browser.start()` with a
matching `browserSession.stop()` (or the language's equivalent) so the daemon
doesn't outlive the script — running the same script twice in a row otherwise leaves
orphaned browser processes around.

## Element references (`@eN`)

Most UI automation tools want a CSS selector for every interaction. Vibium
takes a different approach: it numbers the interactive elements on the current
page and lets you refer to them by short, stable IDs.

```
@e1  link    "Sign in"
@e2  input   placeholder="Email"
@e3  button  "Continue"
```

You get these IDs by running [`vibium map`](commands/map.md), or by calling
[`vibium find ...`](commands/find.md) which returns a reference for each match.

References are stable across commands as long as the page does not change
substantially. Each `map` or `find` refreshes the current reference set, so
an `@eN` reference only means what it meant in the last result you saw. When
the DOM shifts, run `map` again (or `diff map` to see what moved) to refresh
them.

## Semantic finding

Vibium's `find` subcommands match elements the way a human would describe
them: visible text, form labels, placeholders, ARIA roles. CSS selectors are
intentionally not the primary interface — they are brittle and they don't
match how an agent reads a page.

| Subcommand                          | Matches                                |
| ----------------------------------- | -------------------------------------- |
| `vibium find text "Sign in"`        | Visible text content                   |
| `vibium find label "Email"`         | Inputs whose label is "Email"          |
| `vibium find placeholder "Search"`  | Inputs with that placeholder           |
| `vibium find role button`           | Elements with that ARIA role           |

## Verbs and subverbs

A few Vibium commands are actually small command groups:

- `vibium find` has subcommands `text`, `label`, `placeholder`, `role`.
- `vibium wait` is overloaded — `vibium wait "<selector>"` waits for a CSS
  selector, while `vibium wait text "<text>"` and `vibium wait url "<path>"`
  use named subcommands.
- `vibium record` has `start` and `stop`.

That means `vibium wait "h2"` and `vibium wait text "h2"` do different
things: the first waits for any element matching the CSS selector `h2`, the
second waits for the literal string `h2` to appear in the visible page.
When in doubt, the [Command Reference](/docs/commands/) shows the
exact synopsis for each command.

## Standards-based protocol

Under the hood, Vibium speaks [WebDriver BiDi](https://w3c.github.io/webdriver-bidi/),
the W3C bidirectional WebDriver protocol. That means:

- It is a **standard**, not a vendor-specific debugging protocol.
- Future browser support comes "for free" as more browsers ship BiDi.
- You can mix Vibium with other BiDi-aware tools if you ever need to.

## Capture vs. interaction

Vibium splits into two clean halves:

- **Interaction** — `go`, `click`, `fill`, `select`, `check`, `press`, `wait`.
- **Capture** — `text`, `screenshot`, `pdf`, `eval`, `record`.

This makes it easy to reason about side effects: capture commands never change
the page; interaction commands always do.

## MCP server mode

`vibium mcp` starts an MCP (Model Context Protocol) server that exposes the
same commands as MCP tools. Plug it into Codex, Claude Code, Cline, Cursor, or
another MCP-aware client and the browser becomes part of the agent's tool
inventory.
See [MCP Server Integration](mcp-integration.md).
