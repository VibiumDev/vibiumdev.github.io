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
    --ai-base-url string        Override the AI provider's API base URL for this call (the model endpoint, not the site under test); an empty value resets the provider default
    --base-url string           Site under test: opened first unless the current page already shares its origin; relative navigation paths resolve against it
-i, --input string              Read an existing Vibium recording or Playwright trace ZIP; no browser is launched
    --keep-open                 Leave a browser started by Check open after the run (existing browsers are always preserved)
    --model string              Override the model for this call
-o, --output string             Save a new recording ZIP of live verification; an active recording is exported without stopping it (current chunk, no video)
    --provider string           Override the provider for this call; changing provider requires --model and resets endpoint/effort defaults
    --reasoning-effort string   Override OpenAI-compatible reasoning effort; an empty value uses the model default
    --report string             Save the verdict and concise evidence as a new JSON file
```

New in nightly (not yet in the npm release): `--ai-base-url`, `--base-url`, `--input`, `--keep-open`, `--model`, `--output`, `--provider`, `--reasoning-effort`, `--report`

## Description

Asks a fresh AI verifier to investigate a claim and return **PASS**,
**FAIL**, or **INCONCLUSIVE**, with evidence. Live checks use the existing
browser session; `-i` checks a saved recording instead. Requires a
configured model provider — see [Run and Check](../run-and-check.md).

> Looking for the old checkbox command? Toggling checkboxes is now
> `vibium set` and `vibium unset`.

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
