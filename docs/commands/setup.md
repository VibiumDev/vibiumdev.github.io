---
title: vibium setup
---

Interactive setup for AI settings, agent skills, and the local browser.

## Synopsis

```
vibium setup [browser|ai|skills] [flags]
```

## Flags

```
    --non-interactive   Never prompt
    --quick             Only fill what is missing
```

## Examples

```sh
vibium setup
# AI, skills, browser, then readiness. Prompts on a terminal.

vibium setup --non-interactive
# Never prompts; skips AI questions and leaves existing files alone.

vibium setup --quick
# Only fill what is missing.

vibium setup ai
# Provider, model, and API key only.
```
