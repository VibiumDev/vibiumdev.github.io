---
title: MCP Client Setup
description: Register the Vibium MCP server with Claude Code, Claude Desktop, Gemini CLI, or any MCP client that speaks stdio.
---

Every client needs the same thing: the command that starts the server.

```sh
npx -y vibium mcp
```

Chrome for Testing downloads on first use. Tool discovery happens when the
client starts, so open a new session after you add or change the server.

## Claude Code

```sh
claude mcp add vibium -- npx -y vibium mcp
```

Remove it with `claude mcp remove vibium`.

Claude Code can also use Vibium through the CLI and agent skills instead of
MCP; see [Install as an agent skill](../installation.md#install-as-an-agent-skill).

## Claude Desktop

Open **Settings → Developer → Edit Config**. Add the `vibium` entry to
`mcpServers`, keeping any servers already there:

```json
{
  "mcpServers": {
    "vibium": {
      "command": "npx",
      "args": ["-y", "vibium", "mcp"]
    }
  }
}
```

Save, fully quit Claude Desktop, and reopen it. Vibium's tools then appear
in the tools list. If `npx` cannot be found, use its absolute path.

## Gemini CLI

```sh
gemini mcp add vibium npx -y vibium mcp
```

Or edit `~/.gemini/settings.json` (or `.gemini/settings.json` in a project)
and add the same `mcpServers` entry shown for Claude Desktop. Remove it
with `gemini mcp remove vibium`.

## Any other client

Any client that can spawn an MCP server over stdio works. Give it the
command `npx` with the arguments `-y vibium mcp`. If Vibium is installed
globally, the command is `vibium` with the argument `mcp`.

## Try it

Ask the agent:

```text
Use Vibium's browser tools to open https://example.com, take a screenshot,
and summarize the page. Close the browser session you started afterward.
```

A Chrome window opens, the page loads, and the agent replies with the
summary.

## Server options

Append flags to the server command.

| Flag | Effect |
| --- | --- |
| `--headless` | Run the browser without a visible window |
| `--screenshot-dir <dir>` | Save screenshots there. Pass `""` to return them inline only |
| `--engine firefox` | Use Firefox instead of Chrome |

```sh
claude mcp add vibium -- npx -y vibium mcp --headless --screenshot-dir ./screenshots
```

To run your own build, replace `npx -y vibium` with the path to the binary:

```sh
claude mcp add vibium -- /path/to/vibium mcp
```

## Run and Check settings

> **Nightly only.** See [Run and Check](../run-and-check.md).

`vibium_run` and `vibium_check` read AI settings from the server's
environment. In a JSON config, add an `env` object next to `command` and
`args`:

```json
{
  "VIBIUM_AI_PROVIDER": "openai",
  "VIBIUM_AI_MODEL": "your-model",
  "OPENAI_API_KEY": "your-api-key"
}
```

Keep real keys in this local config, not in chat or project files. Restart
the client after changing it. See [Model providers](../ai-providers.md).

## Troubleshooting

**The agent says the tool is not registered.** Check the client's MCP list
(`claude mcp list`), re-register, and start a new session.

**The server does not start.** Run it directly to see the error:

```sh
npx -y vibium mcp
```

It should start and wait for input. Press Ctrl+C to exit.

**The browser does not download or launch.** Install it explicitly:

```sh
npx -y vibium install
```

**Check the server answers.** Send one JSON-RPC message:

```sh
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"capabilities":{}}}' | npx -y vibium mcp
```

The reply is a JSON object with `serverInfo` and `capabilities`.
