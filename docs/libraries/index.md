---
title: Client Libraries
description: Drive Vibium from JavaScript, TypeScript, Python, or Java. Every library wraps the same binary as the CLI.
---

Vibium has first-class libraries for JavaScript/TypeScript, Python, and
Java. Each one wraps the same `vibium` binary the CLI uses, so behavior is
the same on every surface.

| Language | Package | Start here |
| --- | --- | --- |
| JavaScript / TypeScript | `vibium` on npm | [JavaScript](javascript/index.md) |
| Python | `vibium` on PyPI | [Python](python/index.md) |
| Java | `com.vibium:vibium` on Maven Central | [Java](java/index.md) |

## Install

```sh title="JavaScript"
npm install vibium
```

```sh title="Python"
pip install vibium
```

```groovy title="Java"
implementation 'com.vibium:vibium:26.8.21'
```

The browser (Chrome for Testing) downloads on first launch. No driver setup
is needed.

## First script

Open a page, save a screenshot, click a link.

```javascript
import { writeFileSync } from 'node:fs'
import { browser } from 'vibium'

const bro = await browser.start()
const vibe = await bro.page()

await vibe.go('https://example.com')
writeFileSync('screenshot.png', await vibe.screenshot())

const link = await vibe.find({ role: 'link' })
console.log('Found link:', await link.text())
await link.click()

await bro.stop()
```

```python
from vibium import browser

bro = browser.start()
vibe = bro.page()

vibe.go("https://example.com")
with open("screenshot.png", "wb") as f:
    f.write(vibe.screenshot())

link = vibe.find(role="link")
print("Found link:", link.text())
link.click()

bro.stop()
```

```java
import com.vibium.Vibium;
import com.vibium.types.SelectorOptions;
import java.nio.file.Files;
import java.nio.file.Path;

public class Hello {
    public static void main(String[] args) throws Exception {
        var bro = Vibium.start();
        var vibe = bro.page();

        vibe.go("https://example.com");
        Files.write(Path.of("screenshot.png"), vibe.screenshot());

        var link = vibe.find(new SelectorOptions().role("link"));
        System.out.println("Found link: " + link.text());
        link.click();

        bro.stop();
    }
}
```

## The object model

All three libraries share one shape:

- **Browser**: `browser.start()` launches a browser (or attaches to a
  running one) and `stop()` shuts it down.
- **Page**: `bro.page()` returns the default tab. `newPage()` /
  `new_page()` opens another, with its own element references.
- **Element**: `vibe.find(...)` returns an element. Actions such as
  `click()`, `fill(value)`, and `text()` live on the element.

Use one `browser.start()` per process and one page per logical task.

## Sync and async

| Language | Default import | Other flavor |
| --- | --- | --- |
| JavaScript | `vibium` is async (`await` every call) | `vibium/sync` blocks, for scripts and the REPL |
| Python | `vibium` is sync | `vibium.async_api` is async |
| Java | Sync only | |

## How CLI commands map to library calls

| CLI | JavaScript | Python | Java |
| --- | --- | --- | --- |
| `vibium go <url>` | `vibe.go(url)` | `vibe.go(url)` | `vibe.go(url)` |
| `vibium find role link` | `vibe.find({ role: 'link' })` | `vibe.find(role="link")` | `vibe.find(new SelectorOptions().role("link"))` |
| `vibium click <sel>` | `el.click()` | `el.click()` | `el.click()` |
| `vibium fill <sel> <value>` | `el.fill(value)` | `el.fill(value)` | `el.fill(value)` |
| `vibium text <sel>` | `el.text()` | `el.text()` | `el.text()` |
| `vibium eval <js>` | `vibe.evaluate(js)` | `vibe.evaluate(js)` | `vibe.evaluate(js)` |
| `vibium screenshot` | `vibe.screenshot()` | `vibe.screenshot()` | `vibe.screenshot()` |

`vibium map` and its `@e1` references are a CLI and MCP feature. Libraries
hold element objects instead.

## Run and Check from code

> Nightly builds and the next release; see [Run and Check](../run-and-check.md).

The AI-driven operations are client methods on both Browser and Page. In
JavaScript and Python the connected object is also callable as a shorthand
for `run`:

```js
const vibe = await browser.start()
await vibe('open example.com and find the contact page')   // same as vibe.run(...)
const verdict = await vibe.check('the page lists an email address')
```

See [Run and Check](../run-and-check.md) and
[Model providers](../ai-providers.md) for configuration and per-call
`provider`/`model` overrides.

## Custom binary

The Python and Java clients honor `VIBIUM_BIN_PATH`. Point it at your own
build of the binary:

```sh
export VIBIUM_BIN_PATH=/path/to/your/vibium
```
