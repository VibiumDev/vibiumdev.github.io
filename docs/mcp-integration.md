---
title: MCP Server Integration
---

Vibium ships an MCP (Model Context Protocol) server so AI agents can drive
the browser as a first-class tool, alongside their other tools.

## What you get

When Vibium is registered as an MCP server, the agent gains tools that map
1:1 to the CLI commands: navigation, mapping, finding, clicking, filling,
capture, and so on. The agent can use them directly without spawning shell
subprocesses. On nightly builds, the AI-driven
[`run` and `check`](run-and-check.md) operations are exposed too, as
`vibium_run` and `vibium_check`.

## Registering Vibium

### Claude Code

```sh
claude mcp add vibium -- npx -y vibium mcp
```

### Gemini/Antigravity

```sh
gemini mcp add vibium npx -y vibium mcp
```

### Other MCP-aware clients

Any client that can spawn an MCP server over stdio can use Vibium. The
command to spawn is:

```sh
npx -y vibium mcp
```

or, if you have already installed Vibium globally:

```sh
vibium mcp
```

Useful flags: `--headless` hides the browser window, `--screenshot-dir`
changes where screenshots are saved (pass `""` to disable saving), and
`--engine firefox` switches the browser engine.

## What runs where

The MCP server runs locally as a subprocess of your client. It manages the
same browser daemon the CLI uses, so:

- CLI commands and MCP-driven commands share state.
- A screenshot or recording started from one interface is visible to the other.
- Stopping the server stops the client end, not the browser daemon.

## Using it from an agent

Inside an agent, the tools appear with `browser_` names
(`browser_navigate`, `browser_find`, `browser_click`, `browser_fill`,
`browser_screenshot`, `browser_get_text`, …). The agent's tool-use loop is:

1. Call `browser_navigate` with a URL.
2. Call `browser_map` (or `browser_find`) to discover references.
3. Call `browser_click` / `browser_fill` / `browser_select` to interact.
4. Call `browser_get_text` / `browser_screenshot` to read the result.

Or hand over a whole goal at once: `vibium_run` drives the browser toward a
goal, and `vibium_check` independently verifies a claim. Both take optional
per-call `provider`/`model` overrides; see
[Model providers](ai-providers.md).

This is the same loop documented in [Getting Started](getting-started.md);
MCP just removes the shell from the middle.

## Troubleshooting

If the agent reports that the tool isn't registered, confirm with your
client's `mcp list` (or equivalent) command, then try re-registering. If the
server fails to start, run `vibium mcp` directly to surface any error
messages, and check that the bundled browser has been downloaded by running
a quick `vibium go https://example.com` first.
