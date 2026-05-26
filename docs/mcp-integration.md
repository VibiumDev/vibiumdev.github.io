---
title: MCP Server Integration
---

Vibium ships an MCP (Model Context Protocol) server so AI agents can drive
the browser as a first-class tool, alongside their other tools.

## What you get

When Vibium is registered as an MCP server, the agent gains tools that map
1:1 to the CLI commands: navigation, mapping, finding, clicking, filling,
capture, and so on. The agent can use them directly without spawning shell
subprocesses.

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

## What runs where

The MCP server runs locally as a subprocess of your client. It manages the
same browser daemon the CLI uses, so:

- CLI commands and MCP-driven commands share state.
- A screenshot or recording started from one interface is visible to the other.
- Stopping the server stops the client end, not the browser daemon.

## Using it from an agent

Inside an agent, the tools generally appear with names matching the CLI
verbs (`go`, `map`, `find`, `click`, `fill`, `screenshot`, `text`, …). The
agent's tool-use loop is:

1. Call `go` with a URL.
2. Call `map` (or `find`) to discover references.
3. Call `click` / `fill` / `select` to interact.
4. Call `text` / `screenshot` to read the result.

This is the same loop documented in [Getting Started](getting-started.md);
MCP just removes the shell from the middle.

## Troubleshooting

If the agent reports that the tool isn't registered, confirm with your
client's `mcp list` (or equivalent) command, then try re-registering. If the
server fails to start, run `vibium mcp` directly to surface any error
messages, and check that the bundled browser has been downloaded by running
a quick `vibium go https://example.com` first.
