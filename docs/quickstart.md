---
title: Quickstart
---

The shortest possible end-to-end session.

## CLI (installed)

```sh
npm install -g vibium
vibium go https://example.com
vibium screenshot -o example.png
vibium text
```

Open a page, save a screenshot, print the page text. That is the entire
quickstart.

> **Why does `vibium text` not need a URL or selector?** Vibium keeps a
> background browser running across commands; later commands act on the
> page opened by the most recent `vibium go`. See
> [Core Concepts](concepts.md) for the full mental model.

What you should see:

- `vibium go https://example.com` — exits with status 0; the browser
  navigates to the page. No output on stdout is normal.
- `vibium screenshot -o example.png` — writes the PNG to
  `~/Pictures/Vibium/example.png` and prints the saved path to stdout. The
  CLI manages screenshot storage for you; `-o` controls the *filename*, not
  the directory. `ls -lh ~/Pictures/Vibium/example.png` should show a
  non-empty PNG.
- `vibium text` — prints the visible page text to stdout. For
  `https://example.com` you'll see the heading "Example Domain" followed by
  the standard placeholder paragraph.

If any of those don't match, see [Troubleshooting](troubleshooting.md).

## CLI (zero-install with `npx`)

If you'd rather not install anything, the same flow works through `npx`:

```sh
npx -y vibium go https://example.com
npx -y vibium screenshot -o example.png
npx -y vibium text
```

This is great for CI jobs, throwaway scripts, and demos. To make the rest of
this guide copy-pasteable, alias it for the current shell:

```sh
alias vibium='npx -y vibium'
vibium go https://example.com
vibium text
```

## JavaScript / TypeScript

```js
import { writeFileSync } from 'node:fs'
import { browser } from 'vibium'

const browserSession = await browser.start()
const vibe = await browserSession.page()

await vibe.go('https://example.com')
const png = await vibe.screenshot()
writeFileSync('example.png', png)

await browserSession.stop()
```

`screenshot()` returns the PNG as bytes; you have to write them to disk
yourself (unlike the CLI's `-o` flag).

## Python

```python
from vibium import browser

browser_session = browser.start()
vibe = browser_session.page()

vibe.go("https://example.com")
text = vibe.text()
print(text)

browser_session.stop()
```

## Java

```java
var browserSession = Vibium.start();
var vibe = browserSession.page();
vibe.go("https://example.com");
var png = vibe.screenshot();
java.nio.file.Files.write(java.nio.file.Path.of("example.png"), png);
browserSession.stop();
```

## Agent skill for Codex

```sh
npm install -g vibium
npx skills add https://github.com/VibiumDev/vibium --skill vibe-check
```

After this, your agent can drive the browser by emitting `vibium ...` commands.

See the [Tutorial](tutorial.md) for a longer worked example.
