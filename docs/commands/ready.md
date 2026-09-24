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

## Flags

```
    --ai-base-url string        Override the AI provider's API base URL for this call (the model endpoint, not the site under test); an empty value resets the provider default
    --model string              Override the model for this call
    --provider string           Override the provider for this call; changing provider requires --model and resets endpoint/effort defaults
    --reasoning-effort string   Override OpenAI-compatible reasoning effort; an empty value uses the model default
```

## Subcommands

### vibium ready ai

Require valid AI configuration and test authentication, model access, tool calling, and a structured response.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium ready ai [provider] [flags]
```

#### Flags

```
    --ai-base-url string        Override the AI provider's API base URL for this call (the model endpoint, not the site under test); an empty value resets the provider default
    --model string              Override the model for this call
    --provider string           Override the provider for this call; changing provider requires --model and resets endpoint/effort defaults
    --reasoning-effort string   Override OpenAI-compatible reasoning effort; an empty value uses the model default
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
