---
title: vibium run
sidebar:
  badge: Nightly
---

Accomplish a live browser goal using VIBIUM_AI_* configuration.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium run "<goal>" [flags]
```

## Flags

```
    --ai-base-url string        Override the AI provider's API base URL for this call (the model endpoint, not the site under test); an empty value resets the provider default
    --base-url string           Site under test: opened first unless the current page already shares its origin; relative navigation paths resolve against it
    --keep-open                 Keep a browser started by Run open after saving evidence
    --model string              Override the model for this call
-o, --output string             Save a new live recording ZIP; an active recording exports its current chunk without continuous video
    --provider string           Override the provider for this call; changing provider requires --model and resets endpoint/effort defaults
    --reasoning-effort string   Override OpenAI-compatible reasoning effort; an empty value uses the model default
```

## Examples

```sh
vibium run "change my timezone to America/Chicago"
# Accomplishes the goal in the existing browser and reports its result.
vibium run "open https://example.com" -o run.zip --keep-open
# Saves the live recording and leaves a newly started browser open.
vibium run "change my timezone to America/Chicago and save it" --provider local --model my-model --ai-base-url http://127.0.0.1:8080/v1 --reasoning-effort ""
# Uses these settings for one invocation; credentials still come from the environment.
vibium run "add a battery pack to the cart" --base-url http://localhost:3000
# Accomplishes the goal against that site; a page already on its origin keeps its state.
```
