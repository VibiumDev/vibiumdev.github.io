---
title: Installation
---

Vibium ships as a single self-contained binary. The installer also downloads
a managed copy of Google Chrome for Testing on first use, so a fresh install
is a one-liner.

## Prerequisites

- Node.js 18+ (only required for the npm-based installer and the JS client)
- A supported platform: Linux x64, macOS x64/arm64, or Windows x64

You do **not** need a pre-installed browser; Vibium downloads Google Chrome
for Testing.

## Install the CLI

```sh
npm install -g vibium
```

This installs the `vibium` binary globally. The first time you run any command
that requires a browser, Vibium downloads its managed Google Chrome for
Testing build. On macOS, the browser appears as "Google Chrome for Testing".

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

If you are setting up Vibium for an AI coding agent (for example Claude Code),
install it as a skill so the agent learns the full command set:

```sh
npx skills add https://github.com/VibiumDev/vibium --skill vibe-check
```

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
implementation 'com.vibium:vibium:26.3.18'
```

Each client library bundles or locates the same `vibium` binary, so a single
install gives you both the CLI and the programmatic API.

## Verify the installation

```sh
vibium go https://example.com
vibium text
```

If `vibium text` prints the page text, the install succeeded.

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
