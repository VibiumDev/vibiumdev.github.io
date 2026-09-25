---
title: vibium check
---

Check a claim in a live browser or an existing recording with an independent model.

## Synopsis

```
vibium check "<claim>" [flags]
```

## Flags

```
    --base-url string   Site under test: opened first unless the current page already shares its origin; relative navigation paths resolve against it
-i, --input string      Read an existing Vibium recording or Playwright trace ZIP; no browser is launched
    --keep-open         Leave a browser started by Check open after the run (existing browsers are always preserved)
-o, --output string     Save a new recording ZIP of live verification; an active recording is exported without stopping it (current chunk, no video)
    --report string     Save the verdict and concise evidence as a new JSON file
```

## AI Flags

```
--ai-base-url string        AI provider API base URL, not the site under test (env: VIBIUM_AI_BASE_URL); empty resets the provider default
--model string              Model ID for the provider; see Model IDs below (env: VIBIUM_AI_MODEL)
--provider string           AI provider: openai, xai, anthropic, google, openai-compatible, or local (env: VIBIUM_AI_PROVIDER); changing it requires --model and resets endpoint/effort defaults
--reasoning-effort string   none, minimal, low, medium, high, xhigh, or max; not for anthropic or google (env: VIBIUM_AI_REASONING_EFFORT); empty uses the model default
```

## Model IDs

```
openai              https://developers.openai.com/api/docs/models
xai                 https://docs.x.ai/developers/models
anthropic           https://platform.claude.com/docs/en/models/overview
google              https://ai.google.dev/gemini-api/docs/models
openai-compatible   the model name your server serves
local               the model name your server serves
```

New in nightly (not yet in the npm release): `--ai-base-url`, `--base-url`, `--input`, `--keep-open`, `--model`, `--output`, `--provider`, `--reasoning-effort`, `--report`

## Description

Asks a fresh AI verifier to investigate a claim and return **PASS**,
**FAIL**, or **INCONCLUSIVE**, with evidence. Live checks use the existing
browser session; `-i` checks a saved recording instead. Requires a
configured model provider — see [Run and Check](../run-and-check.md).

> In `vibium@26.8.21` (the current npm release), `vibium check` still
> toggles a checkbox (`uncheck` unchecks). The AI check above — and the
> `set`/`unset` checkbox commands that replace the old names — are in the
> nightly builds and the next release.

## Examples

```sh
vibium check "the saved timezone is America/Chicago after refresh"
```

Check saved evidence instead of the live browser:

```sh
vibium check "the order confirmation was shown" -i record.zip
```

## See also

- [Run and Check](../run-and-check.md)
- [Model Providers](../ai-providers.md)
