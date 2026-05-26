---
title: vibium mcp
---

Start the MCP (Model Context Protocol) server.

## Synopsis

```
vibium mcp
```

## Description

Runs Vibium as an MCP server over stdio so that any MCP-aware client (Codex,
Claude Code, Cline, Cursor, Antigravity, etc.) can drive the browser as a tool.
The server exposes the same operations as the CLI: navigation, mapping,
finding, clicking, filling, capture, and so on.

You normally do not invoke `vibium mcp` directly. Instead, register it with
your client and let the client manage its lifecycle. See
[MCP Server Integration](../mcp-integration.md) for the registration
recipes.

## Examples

Register with Claude Code:

```sh
claude mcp add vibium -- npx -y vibium mcp
```

Register with Antigravity/Gemini:

```sh
gemini mcp add vibium npx -y vibium mcp
```

## See also

- [MCP Server Integration](../mcp-integration.md)
