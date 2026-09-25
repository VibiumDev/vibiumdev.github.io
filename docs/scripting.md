---
title: Scripting and Agents
---

Everything an agent or script needs to consume Vibium's output reliably:
the JSON envelope, exit codes, and the machine-readable endpoints this site
publishes.

## JSON output

Every command accepts the global `--json` flag and prints one envelope:

```json
{"ok": true, "result": { ... }}
```

Execution errors print `{"ok": false, "error": "..."}` instead. `ok` means
the command completed, not that the outcome was what you wanted — verdicts
and answers live inside `result`.

```sh
vibium --json url
# {"ok":true,"result":{"url":"https://example.com/"}}
```

## Exit codes

| Command | Exit 0 | Exit 1 |
| ------- | ------ | ------ |
| Most commands | Completed | Failed (bad selector, timeout, browser error) |
| `run` | Operation completed, whether the status is `completed` or `not_completed` | Configuration, provider, browser, or timeout failure |
| `check` | Verdict delivered: PASS, FAIL, or INCONCLUSIVE | Execution failure, no verdict |
| `ready`, `ready ai`, `ready browser` | Ready | Setup problem |
| `is-installed` | Browser installed | Not installed |
| `is visible` / `enabled` / `set` / `actionable` | Answer printed (`true` or `false`) | Only with `--fail`: the answer was `false` |

The `run`/`check` rule matters most for automation: **do not treat exit 0 as
success of the goal or claim**. Inspect the JSON instead:

```sh
vibium check "the cart shows one item" --json
# exit 0 even for FAIL; require result.status == "passed"
vibium run "add a battery pack to the cart" --json
# exit 0 even for not_completed; require result.status == "completed"
```

`is ...` subcommands print `true`/`false` and exit 0 either way; add
`--fail` to turn a `false` answer into exit 1 for shell conditionals.

## Machine-readable docs

This site publishes several endpoints meant for agents:

| URL | Contents |
| --- | -------- |
| [`/commands.json`](https://vibium.com/commands.json) | Every command with usage, flags, and nightly-only markers, generated from the binaries |
| [`/llms.txt`](https://vibium.com/llms.txt) | Curated Markdown index of these docs |
| [`/llms-full.txt`](https://vibium.com/llms-full.txt) | The whole documentation as one file |
| `/llms/docs/....md` | Clean Markdown copy of any page (linked via `rel="alternate"` in each page head) |
| [`/skills/browser.md`](https://vibium.com/skills/browser.md) | The Vibium browser skill, as installed by `vibium add-skill` |
| [`/skills/check.md`](https://vibium.com/skills/check.md) | The check skill for independent verification |

The skills are the fastest way to teach an agent the CLI: they contain the
full command reference with usage patterns. `vibium add-skill` installs the
same content locally for Claude Code and Grok.

## See also

- [Run and Check](run-and-check.md) — the result contract in detail.
- [Command Reference](/docs/commands/) — per-command flags and examples.
