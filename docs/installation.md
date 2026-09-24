---
title: Installation
---

Vibium ships as a single self-contained binary. The installer also downloads
a managed copy of Google Chrome for Testing on first use, so a fresh install
is a one-liner.

## Prerequisites

- Node.js 18+ (only required for the npm-based installer and the JS client)
- A supported platform: Linux x64/arm64, macOS x64/arm64, or Windows x64

You do **not** need a pre-installed browser; Vibium downloads Google Chrome
for Testing. Firefox is also supported — see
[Browser engines](#browser-engines) below.

## Install the CLI

```sh
npm install -g vibium
```

This installs the `vibium` binary globally. The first time you run any command
that requires a browser, Vibium downloads its managed Google Chrome for
Testing build. On macOS, the browser appears as "Google Chrome for Testing".

### Guided setup

> `vibium setup` and `vibium ready` are in the [nightly builds](nightly.md)
> and the next npm release.

After installing, `vibium setup` walks you through the rest in one step: it
prompts for AI settings (used by [`run` and `check`](run-and-check.md)),
installs agent skills for agents already present on the machine, downloads
the browser, and finishes with a readiness check:

```sh
vibium setup
```

Every part is optional and can run on its own (`vibium setup browser`,
`vibium setup ai`, `vibium setup skills`). In CI or from an agent, use
`vibium setup --non-interactive`.

### Zero-install with `npx`

If you don't want to install anything, every command works through `npx`:

```sh
npx -y vibium go https://example.com
npx -y vibium screenshot -o example.png
npx -y vibium text
```

`npx` fetches the package on demand and runs the binary. The first invocation
is a little slower while npm caches the package; subsequent calls are fast.
This is the most ergonomic way to try Vibium, run a one-off in CI, or
script a quick task on a machine where you can't (or don't want to) install
software globally.

For convenience in a shell, alias it:

```sh
alias vibium='npx -y vibium'
```

After that, every example in these docs that says `vibium ...` works as-is.

## Install as an agent skill

If you are setting up Vibium for an AI coding agent, install its skills so
the agent learns the full command set. Vibium detects Claude Code
(`~/.claude`) and Grok (`~/.grok` or `$GROK_HOME`) and installs the
`browser` and `check` skills for each agent present:

```sh
vibium add-skill
```

Use `--agent claude`, `--agent grok`, or `--agent all` to choose explicitly.
`vibium setup` runs the same installation as part of guided setup.

## Browser engines

Chrome is the default engine. Firefox is supported as an alternative, using
Firefox's native WebDriver BiDi — no driver binary involved:

```sh
vibium install --engine firefox
```

Each engine auto-installs on first launch on macOS and Linux, so an explicit
`vibium install` is only needed to pre-download. Every command accepts
`--engine chrome|firefox`, or set `VIBIUM_ENGINE=firefox` once. On Windows,
Firefox auto-install is not available: install Firefox yourself and point
`VIBIUM_ENGINE_PATH` at `firefox.exe`.

`--channel` (or `VIBIUM_ENGINE_CHANNEL`) selects the Firefox release
channel (`release` or `beta`). On [nightly builds](nightly.md), channels
extend to Chrome (`stable`, `beta`, `dev`, `canary`), Vibium installs the
known-good browser version baked into the release by default, and
`VIBIUM_ENGINE_VERSION` pins an exact version for CI fleets.
See [Using Firefox](using-firefox.md) for details.

## Install a client library

Pick the language you want to drive Vibium from:

```sh
# JavaScript / TypeScript
npm install vibium

# Python
uv add vibium
```

Java (Gradle):

```groovy
implementation 'com.vibium:vibium:26.8.21'
```

Each client library bundles or locates the same `vibium` binary, so a single
install gives you both the CLI and the programmatic API.

## Verify the installation

```sh
vibium go https://example.com
vibium text
```

If `vibium text` prints the page text, the install succeeded. On nightly
builds, `vibium ready` runs the same verification as a proper diagnostic:
it checks the installed browser files (and, if configured, the AI provider
for `run` and `check`) and prints what is missing.

## Custom binary path

The Python and Java clients respect the `VIBIUM_BIN_PATH` environment variable,
which lets you point at a custom build of the binary instead of the bundled
copy. This is mostly useful for contributors and CI.

```sh
export VIBIUM_BIN_PATH=/path/to/your/vibium
```

## Updating

Update via the same package manager you used to install:

```sh
npm update -g vibium
# or
uv add --upgrade-package vibium vibium
```

## Uninstalling

```sh
npm uninstall -g vibium
```

The bundled browser lives in Vibium's data directory; remove that directory
to fully reclaim disk space.
