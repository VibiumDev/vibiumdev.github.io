---
title: Run and Check
---

Two commands hand the browser to an AI model instead of you scripting each
step:

- `vibium run "<goal>"` uses the live browser to carry out a goal and returns
  **COMPLETED** or **NOT_COMPLETED**, with concise evidence.
- `vibium check "<claim>"` asks a fresh verifier to investigate a claim and
  returns **PASS**, **FAIL**, or **INCONCLUSIVE**, with evidence. It can check
  the live browser or a saved recording.

They share one AI configuration but never share a conversation, so a Check is
an independent second opinion on a Run.

## Configure once

`vibium setup` prompts for provider, model, and API key and writes
`~/.config/vibium/ai.env` (mode 0600); later commands load empty AI variables
from that file automatically. Then confirm readiness:

```sh
vibium ready ai
```

READY means the provider, model, and tool support all checked out (it makes
up to two small model requests). Supported providers are OpenAI, Anthropic,
Google, xAI, and any OpenAI-compatible or local server — see
[Model providers](ai-providers.md) for environment variables and per-call
overrides.

## Run a goal

Navigate to your app, then describe the change you want:

```sh
vibium go http://localhost:3000/account
vibium run "change my timezone to America/Chicago and save it"
```

```
RUN: change my timezone to America/Chicago and save it

COMPLETED

The timezone was changed and saved.
- The account page reports the saved timezone as America/Chicago.
```

Read the evidence — COMPLETED is the model's assessment, not proof. Run
reuses the existing session and selected page, can change page state, and
does not undo its actions.

`--base-url` names the site under test: it is opened first, and relative
navigation targets resolve against it. (The AI provider endpoint is a
different flag, `--ai-base-url`.)

```sh
vibium run "add a battery pack to the cart" --base-url http://localhost:3000
```

### Shorthand

A quoted multiword prompt is a `run`:

```sh
vibium "open example.com and find its contact page"
```

In JavaScript and Python, a connected Browser or Page is itself callable:
`vibe(goal)` delegates to `vibe.run(goal)`.

## Check a claim

After exercising a flow — by hand, from a script, or via `run` — state the
outcome you want verified:

```sh
vibium check "the saved timezone is America/Chicago after refresh"
```

The verifier starts a fresh conversation, can operate the page (for example,
reload it to check persistence), and may leave it changed. A useful claim
describes a result: "the changed name persists after refresh" goes further
than "clicking Save shows a message".

Check can also assess saved evidence instead of a live browser:

```sh
vibium check "the order confirmation was shown" -i record.zip
```

## Save evidence

Both commands accept `-o` to save a recording of everything the model did:

```sh
vibium run "change my timezone and save it" -o run.zip
vibium check "the timezone persists after refresh" -o check.zip
```

Open the zips in the [Vibium Record Player](https://player.vibium.dev/). If
Run or Check started the browser itself, it closes it when done; add
`--keep-open` to keep it around for inspection, and `vibium stop` to close it
later.

## Exit codes and JSON

Completed operations exit 0 regardless of verdict; execution errors exit 1.
In automation, pass `--json` and inspect the structured result
(`result.status` for Run, the verdict for Check).

## From MCP and the client libraries

MCP exposes `vibium_run` and `vibium_check`. Every client library has
`run()` and `check()` on both Browser and Page:

```js
const result = await page.run('change my timezone to America/Chicago')
console.log(result.status, result.evidence)
```

```python
result = page.check("the saved timezone is America/Chicago")
print(result["status"])
```

All interfaces use the same model budget, action limit, and result contract.

## See also

- [Model providers](ai-providers.md) — providers, env vars, per-call overrides.
- [Recording](recording.md) — what's inside the evidence zips.
