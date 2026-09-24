---
title: Concurrent Sessions
---

One-shot CLI commands (`vibium go`, `vibium click`, `vibium find`, …) share a
background daemon that keeps one browser alive between commands. By default
there is one daemon per host, so two scripts driving the CLI at the same time
would share one browser and interfere with each other.

Named sessions give each script its own daemon and browser.

## Use a session per script

Set `VIBIUM_SESSION` once at the top of a script:

```sh
#!/bin/sh
export VIBIUM_SESSION=checkout-tests

vibium go https://staging.example.com/checkout
vibium fill "#email" "test@example.com"
vibium click "button[type=submit]"

vibium daemon stop   # shut down this session's browser when done
```

Or pass `--session` per command — useful when one script drives two browsers:

```sh
vibium --session buyer go https://shop.example.com
vibium --session seller go https://shop.example.com/admin
```

Both forms are equivalent; the flag takes precedence over the environment.
Session names may use letters, digits, `-` and `_` (max 64 chars).

## Inspecting sessions

Each session has its own daemon, socket, PID file, and idle timeout:

```sh
vibium --session buyer daemon status
```

`vibium daemon stop` stops one session's daemon; other sessions are
unaffected.

## Sessions and Run/Check

[`vibium run` and `vibium check`](run-and-check.md) operate on the session
they are invoked in — keep the same `VIBIUM_SESSION` value for the browser
workflow and its checks.

## Concurrent agents in one browser

Inside a single session, the client libraries give each agent its own
isolated page: `browser.newPage()` returns a page with per-page element
references, so two agents mapping and clicking concurrently do not clobber
each other's `@eN` references.
