---
title: Troubleshooting
---

Quick fixes for the most common issues.

## "command not found: vibium"

The npm global `bin` directory isn't on your `PATH`. Either add it
(`npm config get prefix` will show you where), or skip the global install
entirely and use `npx`:

```sh
npx -y vibium go https://example.com
```

If you plan to use Vibium repeatedly in a session, alias it once:

```sh
alias vibium='npx -y vibium'
```

## The browser doesn't appear

By default Vibium runs a visible browser. If you don't see a window:

- You may be on a headless host (e.g. a CI runner or a remote server with no
  display). That's expected; capture commands like `screenshot` and `text`
  still work.
- Google Chrome for Testing may still be downloading on first use. Re-run the
  command after it finishes.

## "no element matches" from `find`

Vibium matches semantically: visible text, label, placeholder, role. If
nothing matches:

- The page may not be ready yet — try [`vibium wait`](commands/wait.md) before
  finding.
- The text may differ from what you expect — `vibium text` will show you the
  actual rendered content.
- The element may be inside a closed `<details>`, a hidden tab, or a shadow
  root that requires scrolling or expanding first.

## A reference like `@e3` doesn't work anymore

References are stable while the page is unchanged, and each `find` or `map`
output defines the current `@eN` set. If the page navigated or re-rendered,
run [`vibium map`](commands/map.md) (or [`vibium diff map`](commands/diff.md))
to refresh. Get into the habit of running `wait` after any action that
triggers navigation.

## Custom binary path

The Python and Java clients honor `VIBIUM_BIN_PATH` if you need to point at a
locally built binary:

```sh
export VIBIUM_BIN_PATH=/path/to/your/vibium
```

## MCP server won't start

Run the server directly to see the error message:

```sh
vibium mcp
```

If the bundled browser hasn't been downloaded yet, run any normal command
first (for example `vibium go https://example.com`) so the download
completes, then restart your MCP client.

## Recordings are huge

`vibium record` captures a screenshot per step. Long sessions produce big
zips. If you only need a final snapshot, use [`vibium screenshot`](commands/screenshot.md)
instead of `record`.

## Where to ask for help

- **Bugs in the `vibium` binary, library, or MCP server** — file an issue at
  <https://github.com/VibiumDev/vibium/issues>.
- **Mistakes, gaps, or unclear writing in these docs** — file an issue
  against this docs repository.

When reporting a runtime bug, please include:

- Your platform and architecture (`uname -a` or equivalent).
- The exact command you ran and the full output.
- The Vibium version (`vibium --version`).
- A `record.zip` from a `vibium record` session reproducing the problem,
  if you can.
