---
title: MCP Server
description: Vibium ships an MCP server so AI agents can drive a real browser with tool calls instead of shell commands.
---

Vibium ships an MCP (Model Context Protocol) server. Register it with an
AI client and the agent can drive a real browser through tool calls,
next to its other tools.

```sh
npx -y vibium mcp
```

That command is the whole server: JSON-RPC over stdio, no hosted service,
no account. [Client Setup](setup.md) has the exact steps for Claude Code,
Claude Desktop, Gemini CLI, and any other MCP client.

## What the agent gets

The tools mirror the CLI commands, so everything in the
[Command Reference](../commands/index.md) has a tool-call form.

| Tools | What they do |
| --- | --- |
| `browser_start`, `browser_stop` | Start and stop the browser session |
| `browser_navigate`, `browser_back`, `browser_reload` | Move between pages |
| `browser_map`, `browser_find`, `browser_find_all` | Discover elements and get `@e1`-style references |
| `browser_click`, `browser_fill`, `browser_type`, `browser_select`, `browser_keys` | Act on elements |
| `browser_get_text`, `browser_get_html`, `browser_a11y_tree`, `browser_screenshot` | Read the result |
| `browser_new_page`, `browser_list_pages`, `browser_switch_page` | Work with several tabs |
| `vibium_run`, `vibium_check` | Hand over a whole goal, or verify a claim (nightly) |

Run `vibium mcp --help` for the full list with descriptions.

## The tool-use loop

1. Call `browser_navigate` with a URL.
2. Call `browser_map` (or `browser_find`) to discover references.
3. Call `browser_click` / `browser_fill` / `browser_select` to interact.
4. Call `browser_get_text` / `browser_screenshot` to read the result.

A tool call names the tool and passes JSON arguments:

```json title="MCP"
{ "name": "browser_navigate", "arguments": { "url": "https://example.com" } }
```

This is the same loop as the [CLI](../cli/index.md); MCP removes the shell
from the middle.

## Run and Check

> **Nightly only.** See [Run and Check](../run-and-check.md).

`vibium_run` drives the browser toward a goal. `vibium_check` independently
verifies a claim and returns a verdict with evidence. Both use the AI
settings in the server's environment and take optional per-call
`provider`/`model` overrides; see [Model providers](../ai-providers.md).

## What runs where

The MCP server runs locally as a subprocess of your client. It manages the
same browser daemon the CLI uses, so:

- CLI commands and MCP tool calls share state.
- A screenshot or recording started from one interface is visible to the other.
- Stopping the server stops the client end, not the browser daemon.

Screenshots taken through MCP are saved to `~/Pictures/Vibium/`
(`Pictures\Vibium\` on Windows). Change that with `--screenshot-dir`; see
[Client Setup](setup.md#server-options).
