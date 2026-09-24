---
title: Using Firefox
---

Vibium launches Chrome by default. Firefox is supported as an alternative
engine, using Firefox's native WebDriver BiDi — no driver binary involved.

## Install

```sh
vibium install --engine firefox
```

Firefox installs into the Vibium cache next to Chrome for Testing. The
binary auto-installs the selected engine on first launch on macOS and Linux,
so the CLI, MCP, and every client get it for free. On Windows, Firefox
auto-install is not available: install Firefox yourself and point
`VIBIUM_ENGINE_PATH` at `firefox.exe`.

## Launch

Every CLI command accepts `--engine`, or set it once with
`VIBIUM_ENGINE=firefox`:

```sh
vibium start --engine firefox
```

The clients have a named launcher and an engine option:

```js
import { firefox, browser } from 'vibium'
const bro = await firefox.start()
// equivalent: await browser.start({ engine: 'firefox' })
```

```python
from vibium import firefox
bro = firefox.start()
```

```java
Browser bro = Vibium.start(new StartOptions().engine("firefox"));
```

MCP — `browser_start` takes an `engine` argument (`chrome` or `firefox`) and
an optional `channel`.

## Channels and version pinning

`--channel beta` (or `VIBIUM_ENGINE_CHANNEL=beta`) selects the Firefox beta;
for Chrome the channels are `stable`, `beta`, `dev`, and `canary`. Each
channel is cached separately and only the selected one runs, so an installed
beta never shadows stable.

Without a pin, the default channels install the known-good browser version
baked into the Vibium release, so a browser update cannot break installs
before Vibium has tested it. `VIBIUM_ENGINE_VERSION` pins an exact version —
useful for keeping CI fleets on one version until you move the pin.

| Variable | Effect |
|----------|--------|
| `VIBIUM_ENGINE` | Default engine (`chrome` or `firefox`) when `--engine` is not given |
| `VIBIUM_ENGINE_PATH` | Use this Firefox executable instead of the Vibium cache (Firefox only) |
| `VIBIUM_ENGINE_CHANNEL` | Channel to install and run, same as `--channel` |
| `VIBIUM_ENGINE_VERSION` | Pin the exact version to install and run (e.g. `153.0.4`) |

## Feature differences

Almost everything works identically on both engines: navigation, elements,
input, screenshots, dialogs, network events, downloads, storage, and trace
recording. The notable differences:

- **Native video recording** requires Firefox 154+ — Chrome has not
  implemented the BiDi screencast command yet. See [Recording](recording.md).
- **PDF printing** output may differ between engines.
