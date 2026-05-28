---
title: Introduction
---

Vibium is a browser automation tool designed for AI agents and humans.
It gives an agent (or a script) a real browser it can drive: navigate to pages,
fill forms, click buttons, extract text, capture screenshots, and record sessions.

## Why Vibium

- **AI-native**. Install Vibium as a skill and an agent immediately gains the
  full browser-automation toolkit, with command names and semantics designed to
  be intuitive for an LLM.
- **Zero configuration**. A single install pulls down Google Chrome for
  Testing. No driver binaries, no profile setup, no protocol shims to glue
  together.
- **Standards-based**. Built on the [WebDriver BiDi](https://w3c.github.io/webdriver-bidi/)
  protocol rather than a vendor-specific debugging protocol.
- **Lightweight**. A single ~10 MB binary with no runtime dependencies.
- **Multi-interface**. Use Vibium from the [CLI](/docs/commands/), as an
  [MCP server](mcp-integration.md), or as a
  [client library](client-libraries.md) in JavaScript/TypeScript, Python, or
  Java.

## Who it is for

- Agents (Codex, Claude Code, Cline, Antigravity, Cursor, OpenCode, Pi, Amp)
  that need to act on real web pages.
- Test engineers writing AI-native end-to-end tests.
- Developers and humans who want a friendly CLI for ad-hoc browser tasks.

## Platform support

| Platform                       | Support target |
| ------------------------------ | -------------- |
| Linux (x64)                    | Yes            |
| macOS (x64, Intel)             | Yes            |
| macOS (arm64, Apple Silicon)   | Yes            |
| Windows (x64)                  | Yes            |

## Where next

- [Installation](installation.md) — install the binary and the browser.
- [Quickstart](quickstart.md) — open a page and take a screenshot in 30 seconds.
- [Getting Started](getting-started.md) — the mental model and the core command loop.
- [Tutorial](tutorial.md) — a worked end-to-end example.
- [Command Reference](/docs/commands/) — every command, with examples.
