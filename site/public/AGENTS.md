# Vibium — Agent Guide

Vibium is browser automation for AI agents and humans, built on WebDriver
BiDi. This file is the entry point for agents: how to install the CLI,
configure it, drive a browser with it, and where the machine-readable docs
live.

## Surfaces

One binary, five ways to drive it. Pick one and read only its bundle.

| Surface | Install | Start page | Bundle |
| --- | --- | --- | --- |
| CLI | `npm install -g vibium` | [/docs/cli.md](https://vibium.com/docs/cli.md) | [llms-cli.txt](https://vibium.com/llms-cli.txt) |
| MCP | `claude mcp add vibium -- npx -y vibium mcp` | [/docs/mcp/setup.md](https://vibium.com/docs/mcp/setup.md) | [llms-mcp.txt](https://vibium.com/llms-mcp.txt) |
| JavaScript | `npm install vibium` | [/docs/libraries/javascript.md](https://vibium.com/docs/libraries/javascript.md) | [llms-javascript.txt](https://vibium.com/llms-javascript.txt) |
| Python | `pip install vibium` | [/docs/libraries/python.md](https://vibium.com/docs/libraries/python.md) | [llms-python.txt](https://vibium.com/llms-python.txt) |
| Java | `com.vibium:vibium` on Maven Central | [/docs/libraries/java.md](https://vibium.com/docs/libraries/java.md) | [llms-java.txt](https://vibium.com/llms-java.txt) |

Docs pages show examples for every surface. Add `?surface=python` (or
`cli`, `mcp`, `javascript`, `java`, `all`) to a docs URL to filter the HTML
view; the Markdown always carries all of them.

## Installation

```sh
npm install -g vibium
```

Or zero-install: prefix any command with `npx -y` (`npx -y vibium go
https://example.com`). The managed browser (Chrome for Testing) downloads on
first use; `vibium install --engine firefox` adds Firefox. Client libraries:
`npm install vibium` (JS/TS), `uv add vibium` (Python),
`com.vibium:vibium` on Maven Central (Java).

## Configuration

No configuration is needed for direct browser commands. For the AI-driven
`vibium run` and `vibium check` (nightly builds), set `VIBIUM_AI_PROVIDER`,
`VIBIUM_AI_MODEL`, and the provider's API key env var, or run `vibium setup`
to write `~/.config/vibium/ai.env` interactively. Useful env vars:
`VIBIUM_ENGINE` (chrome|firefox), `VIBIUM_SESSION` (isolated concurrent
sessions), `VIBIUM_ENGINE_CHANNEL`. Verify with `vibium ready`.

## Usage

The core loop:

```sh
vibium go https://example.com   # navigate
vibium map                      # list elements as @e1, @e2, ...
vibium click @e2                # act on a reference
vibium text                     # read the result
```

Semantic finding (`vibium find text "Sign in"`, `find label`, `find role`)
beats CSS selectors. Every command accepts `--json` and prints an
`{"ok": true, "result": ...}` envelope; execution errors print
`{"ok": false, "error": "..."}`. Note: `run` and `check` exit 0 whenever
the operation completes, regardless of verdict — inspect `result.status`.
Full contract: [Scripting and Agents](https://vibium.com/docs/scripting.md).

## Machine-readable docs

- [llms.txt](https://vibium.com/llms.txt) — curated Markdown index of the docs
- [llms-full.txt](https://vibium.com/llms-full.txt) — all docs in one file
- `llms-<surface>.txt` — the shared docs plus one surface (see Surfaces)
- [commands.json](https://vibium.com/commands.json) — every CLI command, its
  flags, and nightly-only markers, generated from the binaries
- [Browser skill](https://vibium.com/skills/browser.md) and
  [check skill](https://vibium.com/skills/check.md) — the full agent skills,
  as installed by `vibium add-skill`
- Any docs page is available as Markdown by appending `.md` to its path
  (e.g. `/docs/quickstart.md`), or under `/llms/docs/`
- Discovery: `/.well-known/agent-skills/index.json` (skills index with
  sha256 digests) and `/.well-known/api-catalog` (RFC 9727 linkset)

## Source

- CLI, clients, and MCP server: https://github.com/VibiumDev/vibium
- This docs site: https://github.com/VibiumDev/vibiumdev.github.io
