---
title: Model Providers
---

[Run and Check](run-and-check.md) share one AI configuration. Each invocation
still starts a fresh conversation.

## Shared configuration

| Setting | Environment variable |
|---------|----------------------|
| Provider | `VIBIUM_AI_PROVIDER` |
| Model | `VIBIUM_AI_MODEL` |
| Optional API base URL | `VIBIUM_AI_BASE_URL` |
| Optional reasoning effort | `VIBIUM_AI_REASONING_EFFORT` |

Supported providers, with their credentials:

| Provider | Credential | Default API base URL |
|----------|------------|----------------------|
| `openai` | `OPENAI_API_KEY`, required | `https://api.openai.com/v1` |
| `xai` | `XAI_API_KEY`, or a signed-in Grok CLI session | `https://api.x.ai/v1` |
| `anthropic` | `ANTHROPIC_API_KEY`, required | `https://api.anthropic.com/v1` |
| `google` | `GOOGLE_API_KEY`, or `GEMINI_API_KEY` | `https://generativelanguage.googleapis.com/v1beta` |
| `openai-compatible` | `OPENAI_API_KEY`, optional | Explicit base URL required |
| `local` | `OPENAI_API_KEY`, optional | `http://127.0.0.1:8080/v1` |

`local` targets an OpenAI-compatible server you already run on localhost; it
does not download or launch a model server. Reasoning-effort settings apply
to OpenAI, xAI, and compatible endpoints; leave them unset for Anthropic and
Google.

When `XAI_API_KEY` is unset, Vibium reuses a signed-in Grok CLI session
(read-only — it never refreshes or rewrites that login).

## Writing the configuration

`vibium setup` prompts for these values and writes `~/.config/vibium/ai.env`
(mode 0600, previous copy kept as `.bak`). `vibium config init` writes the
same file as a commented template without prompting. On each command, Vibium
loads that file for AI variables that are empty in the environment; a
nonempty process environment always wins. Set `VIBIUM_LOAD_AI_ENV=0` to skip
loading.

Confirm the configuration with:

```sh
vibium ready ai
```

It lists missing settings and tests the provider's model and tool support
with at most two small requests. Exit 0 means ready.

## Per-call overrides

Run, Check, and `ready ai` accept the same overrides, which apply to that
invocation only:

| CLI flag | JS / MCP / Java option | Python keyword |
|----------|------------------------|----------------|
| `--provider` | `provider` | `provider` |
| `--model` | `model` | `model` |
| `--ai-base-url` | `aiBaseURL` | `ai_base_url` |
| `--reasoning-effort` | `reasoningEffort` | `reasoning_effort` |

```sh
vibium run "change my timezone and save it" --provider anthropic --model your-claude-model
vibium check "the timezone persists after reload" --provider google --model your-gemini-model
```

When the provider changes, supply the model explicitly; Vibium clears the old
provider's model, endpoint, and effort before applying your options.
Credentials always come from the provider's environment variable — there is
no API-key flag.

> Renamed flag: `--base-url` used to mean the AI endpoint. It now names the
> site under test for Run and Check; the AI endpoint is `--ai-base-url`.

## SDK and MCP runtimes

The CLI reads settings on each call. SDK and MCP processes read their
environment at startup — restart them after changing environment defaults.
Per-call overrides take effect immediately either way.
