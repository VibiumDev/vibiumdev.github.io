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
    --base-url string   Site under test: opened first unless the current page already shares its origin; relative navigation paths resolve against it
    --keep-open         Keep a browser started by Run open after saving evidence
-o, --output string     Save a new live recording ZIP; an active recording exports its current chunk without continuous video
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
