---
title: vibium ready
sidebar:
  badge: Nightly
---

Check the selected local browser executable files, then test AI when configured. No browser or driver is launched.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium ready [flags]
vibium ready [command]
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

## Subcommands

### vibium ready ai

Require valid AI configuration and test authentication, model access, tool calling, and a structured response.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium ready ai [provider] [flags]
```

#### AI Flags

```
--ai-base-url string        AI provider API base URL, not the site under test (env: VIBIUM_AI_BASE_URL); empty resets the provider default
--model string              Model ID for the provider; see Model IDs below (env: VIBIUM_AI_MODEL)
--provider string           AI provider: openai, xai, anthropic, google, openai-compatible, or local (env: VIBIUM_AI_PROVIDER); changing it requires --model and resets endpoint/effort defaults
--reasoning-effort string   none, minimal, low, medium, high, xhigh, or max; not for anthropic or google (env: VIBIUM_AI_REASONING_EFFORT); empty uses the model default
```

#### Model IDs

```
openai              https://developers.openai.com/api/docs/models
xai                 https://docs.x.ai/developers/models
anthropic           https://platform.claude.com/docs/en/models/overview
google              https://ai.google.dev/gemini-api/docs/models
openai-compatible   the model name your server serves
local               the model name your server serves
```

```sh
vibium ready ai
# Tests the configured provider and model.
vibium ready ai anthropic --model your-model
# Tests Anthropic with the supplied model and ANTHROPIC_API_KEY.
vibium ready ai xai --model grok-4
# Tests xAI with the supplied model and XAI_API_KEY.
vibium ready ai --json
# Prints the provider checks as JSON.
vibium ready ai --provider local --model my-model --ai-base-url http://127.0.0.1:8080/v1 --reasoning-effort ""
# Uses these settings for one invocation; credentials still come from the environment.
```

### vibium ready browser

List discovered Vibium browser installations and check the selected Chrome or Firefox executable files.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium ready browser [engine] [flags]
```

```sh
vibium ready browser
# Checks the default/selected installation; other discovered installations are informational.
vibium ready browser firefox --channel beta
# Checks Firefox beta installation without launching it or changing defaults.
vibium ready browser chrome --json
# Structured installation results; browser connection is reported as skipped.
```

## Examples

```sh
vibium ready
# Checks browser installation and configured AI; reports fixes or READY.
vibium ready --json
# Structured readiness results; exit 0 when requested checks pass, otherwise 1.
vibium ready --provider local --model my-model --ai-base-url http://127.0.0.1:8080/v1 --reasoning-effort ""
# Uses these settings for one invocation; credentials still come from the environment.
```
