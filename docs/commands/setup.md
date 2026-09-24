---
title: vibium setup
sidebar:
  badge: Nightly
---

Interactive setup for AI settings, agent skills, and the local browser.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

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
