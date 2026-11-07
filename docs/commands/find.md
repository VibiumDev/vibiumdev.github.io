---
title: vibium find
---

Find elements and return @eN refs for later commands.

## Synopsis

```
vibium find [description] [flags]
vibium find [command]
```

## Flags

```
    --all               Find all matching elements
    --details           Print diagnostics: method, model, raw scores
    --limit int         Maximum number of elements to return (with --all) (default 10)
    --strategy string   How to resolve: auto, cv (local image matching only), vlm (vision model only), or tree (page tree only) (default "auto")
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
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

New in nightly (not yet in the npm release): `--ai-base-url`, `--details`, `--model`, `--provider`, `--reasoning-effort`, `--strategy`

## Subcommands

### vibium find alt

Find element by alt attribute.

```
vibium find alt [alt] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find alt "Logo"
```

### vibium find css

Find element by CSS selector.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium find css [css] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find css "button.primary"
# → @e1 [button] "Submit"

vibium find css "a" --all
# → @e1 [a] "Home"  @e2 [a] "About"  ...
```

### vibium find description

Find element by natural-language description.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium find description [description] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
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
vibium find description "the Add to Cart button"
# Same as a bare string; explicit when the text could read as a locator
vibium description --provider local --model my-model --ai-base-url http://127.0.0.1:8080/v1 --reasoning-effort ""
# Uses these settings for one invocation; credentials still come from the environment.
```

### vibium find image

Find where a reference image appears on screen.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium find image [path] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
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
vibium find image ./thumbnail.png
# → @e1 [img] "Product thumbnail"

vibium find image ./thumbnail.png --all --json
# Every occurrence, with bounding boxes

vibium find image ./icon.png --strategy cv
# Local feature matching only; nothing leaves the machine
vibium image --provider local --model my-model --ai-base-url http://127.0.0.1:8080/v1 --reasoning-effort ""
# Uses these settings for one invocation; credentials still come from the environment.
```

### vibium find label

Find input by associated label text.

```
vibium find label [label] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find label "Email"
# → @e1 [input type="email"] placeholder="Email"
```

### vibium find placeholder

Find element by placeholder attribute.

```
vibium find placeholder [placeholder] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find placeholder "Search..."
# → @e1 [input] placeholder="Search..."
```

### vibium find role

Find element by ARIA role.

```
vibium find role [role] [flags]
```

#### Flags

```
    --name string       Accessible name filter
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find role button
# → @e1 [button] "Submit"

vibium find role heading --name "Example"
# Find heading with accessible name "Example"
```

### vibium find tag

Find element by HTML tag name.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium find tag [tag] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find tag h1
# → @e1 [h1] "Example Domain"
```

### vibium find testid

Find element by data-testid attribute.

```
vibium find testid [testid] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find testid "submit-btn"
# → @e1 [button] data-testid="submit-btn"
```

### vibium find text

Find element by text content.

```
vibium find text [text] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find text "Sign In"
# → @e1 [button] "Sign In"
```

### vibium find title

Find element by title attribute.

```
vibium find title [title] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find title "Close"
```

### vibium find xpath

Find element by XPath expression.

```
vibium find xpath [xpath] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find xpath "//div[@class='main']"
# → @e1 [div.main] ...
```

## Description

`find` matches elements the way a human would describe them, returning one or
more `@eN` references you can pass to interaction commands.

| Variant                              | Matches                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------- |
| `vibium find text "<text>"`          | Elements whose visible text contains `<text>`.                          |
| `vibium find label "<label>"`        | Form fields whose `<label>` is `<label>`.                               |
| `vibium find placeholder "<text>"`   | Inputs with that placeholder.                                           |
| `vibium find role <role>`            | Elements with the given ARIA role (`button`, `searchbox`, `link`, …).   |

Each match is printed in the same form as [`vibium map`](map.md): a line per
element with its `@eN` reference, role, and a short description.

## Examples

```sh
vibium find text "Sign in"
vibium find label "Email"
vibium find placeholder "Search..."
vibium find role button
```

Typical workflow — find, then act on the reference:

```sh
$ vibium find label "Email"
@e2  input  label="Email"

$ vibium fill @e2 "alice@example.com"
```

## See also

- [`vibium map`](map.md) — list every element instead of finding one.
- [`vibium click`](click.md), [`vibium fill`](fill.md) — act on the result.
