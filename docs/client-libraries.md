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
implementation 'com.vibium:vibium:26.3.18'
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
Node REPL — see the project README for details.

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

Refer to each language's package documentation for exact method names — the
shape of the API is the same across all three.

## Lifecycle

- `browser.start()` boots a browser process (or attaches to a running one).
- `browserSession.page()` opens a new tab and returns a handle.
- `browserSession.stop()` shuts the browser down cleanly.

You generally want one `browser.start()` per process and one `page()` per
logical session.
