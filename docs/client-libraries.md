---
title: Client Libraries
---

Vibium provides first-class libraries for JavaScript/TypeScript, Python, and
Java. Each one wraps the same underlying binary, so the behavior matches the
CLI exactly.

## Installation

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

## JavaScript / TypeScript (async)

```js
import { browser } from 'vibium'

const browserSession = await browser.start()
const vibe = await browserSession.page()

await vibe.go('https://example.com')
const png = await vibe.screenshot()

await browserSession.stop()
```

The JavaScript client also exposes a synchronous flavor that works well in a
Node REPL — import from `vibium/sync` and drop the `await`s.

To launch Firefox instead of Chrome, use the named launcher or the engine
option:

```js
import { firefox, browser } from 'vibium'

const bro = await firefox.start()
// equivalent:
const bro2 = await browser.start({ engine: 'firefox' })
```

## Python (sync)

```python
from vibium import browser

browser_session = browser.start()
vibe = browser_session.page()

vibe.go("https://example.com")
text = vibe.text()
print(text)

browser_session.stop()
```

The Python client also has an async flavor; the API is the same with `await`
in front of every call.

The Python client locates the bundled Vibium binary automatically. To use a
custom build, set:

```sh
export VIBIUM_BIN_PATH=/path/to/your/vibium
```

## Java

```java
var browserSession = Vibium.start();
var vibe = browserSession.page();

vibe.go("https://example.com");
var png = vibe.screenshot();

browserSession.stop();
```

The published Maven Central artifact bundles native binaries for every
supported platform.

## Mapping CLI commands to library calls

The libraries mirror the CLI:

| CLI                                | Library (Python sync, illustrative)                     |
| ---------------------------------- | ------------------------------------------------------- |
| `vibium go <url>`                  | `vibe.go(url)`                                          |
| `vibium map`                       | `vibe.map()`                                            |
| `vibium find text "<text>"`        | `vibe.find_text(text)`                                  |
| `vibium click @e2`                 | `vibe.click("@e2")`                                     |
| `vibium fill @e3 "<value>"`        | `vibe.fill("@e3", value)`                               |
| `vibium text`                      | `text = vibe.text()`                                    |
| `vibium eval "<js>"`               | `vibe.eval(js)`                                         |
| `vibium run "<goal>"`              | `vibe.run(goal)`                                        |
| `vibium check "<claim>"`           | `vibe.check(claim)`                                     |

Refer to each language's package documentation for exact method names — the
shape of the API is the same across all three.

## Run and Check from code

The AI-driven operations are first-class client methods on both Browser and
Page. In JavaScript and Python the connected object is itself callable as a
shorthand for `run`:

```js
const vibe = await browser.start()
await vibe('open example.com and find the contact page')   // same as vibe.run(...)
const verdict = await vibe.check('the page lists an email address')
```

See [Run and Check](run-and-check.md) and
[Model providers](ai-providers.md) for configuration and per-call
`provider`/`model` overrides.

## Lifecycle

- `browser.start()` boots a browser process (or attaches to a running one).
- `browserSession.page()` opens a new tab and returns a handle.
- `browserSession.stop()` shuts the browser down cleanly.

You generally want one `browser.start()` per process and one `page()` per
logical session. For concurrent agents, `newPage()` gives each its own
isolated page with per-page element references.
