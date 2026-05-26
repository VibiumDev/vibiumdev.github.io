---
title: Getting Started
---

This page walks through your first real session with Vibium. It assumes you
have either [installed](installation.md) the `vibium` binary globally or
are running it via `npx -y vibium ...`. The two are interchangeable; pick
whichever you prefer.

> **Tip.** If you don't want to install anything, alias `npx` for the
> session and the examples below work unchanged:
>
> ```sh
> alias vibium='npx -y vibium'
> ```

## The mental model

A Vibium session is a sequence of CLI commands that share a single browser.
Vibium runs a small daemon in the background to keep the browser alive between
commands, so each invocation is fast and you can interleave commands with
your own scripting.

A typical loop looks like:

1. `vibium go <url>` — open a page.
2. `vibium map` — list interactive elements with stable references like `@e1`,
   `@e2`, `@e3`.
3. `vibium click @e2` or `vibium fill @e3 "..."` — act on those references.
4. `vibium text` or `vibium screenshot` — read the result.

This is the same loop an agent uses; the references are designed to be easy
for an LLM to reason about and stable across commands.

## A first session

Open the Vibium homepage and grab a screenshot:

```sh
vibium go https://example.com
vibium screenshot -o example.png
```

List the interactive elements on the page:

```sh
vibium map
```

You should see lines like:

```
@e1  link   "More information..."  (https://www.iana.org/...)
```

Click the first link by reference:

```sh
vibium click @e1
```

Wait for the new page to settle, then read its text:

```sh
vibium wait text "IANA"
vibium text
```

## Finding things semantically

CSS selectors are brittle. Vibium prefers semantic locators that match what a
human would describe:

```sh
vibium find text "Sign in"
vibium find label "Email"
vibium find placeholder "Search..."
vibium find role button
```

Each `find` returns one or more `@e` references you can then `click`, `fill`,
or otherwise act on.

## What to read next

- [Tutorial](tutorial.md) — a complete form-filling walkthrough.
- [Core Concepts](concepts.md) — references, mapping, daemon mode.
- [Command Reference](/docs/commands/) — every command in detail.

(If you skipped the [Quickstart](quickstart.md), it's a condensed
copy-paste version of this page.)
