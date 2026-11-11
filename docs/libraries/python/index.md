---
title: Python
description: Install the Vibium Python client, run a first script, and choose between the sync and async APIs.
---

The `vibium` package on PyPI drives a real browser from Python. It bundles
the `vibium` binary for your platform.

## Requirements

- Python 3.11 or newer
- Linux x64/arm64, macOS x64/arm64, or Windows x64

## Install

```sh
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install vibium
```

With uv, use `uv add vibium`. Chrome for Testing downloads the first time a
browser starts. To fetch it ahead of time, run `vibium install`.

## First script

Save this as `hello.py`:

```python
from vibium import browser

# Launch a browser. The window is visible by default.
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

Run it:

```sh
python3 hello.py
```

A Chrome window opens, loads the page, clicks the link, and closes. The
script prints `Found link: Learn more` and leaves `screenshot.png` in the
folder.

| Call | What it does |
| --- | --- |
| `browser.start()` | Launches Chrome and returns a Browser |
| `bro.page()` | Returns the default page (tab) |
| `vibe.go(url)` | Navigates to a URL |
| `vibe.screenshot()` | Returns the page as PNG bytes |
| `vibe.find(role="link")` | Finds an element by its accessible role |
| `link.click()` | Clicks the element |
| `bro.stop()` | Closes the browser |

## Async API

The default import is sync. `vibium.async_api` exposes the same API as
coroutines:

```python
import asyncio
from vibium.async_api import browser

async def main():
    bro = await browser.start()
    vibe = await bro.page()
    await vibe.go("https://example.com")
    link = await vibe.find(role="link")
    print(await link.text())
    await bro.stop()

asyncio.run(main())
```

## Options

Hide the browser window:

```python
bro = browser.start(headless=True)
```

Launch Firefox instead of Chrome:

```python
from vibium import firefox

bro = firefox.start()
# same as: browser.start(engine="firefox")
```

See [Using Firefox](../../using-firefox.md) for engine details.

## Finding elements

`find` takes semantic locators as keyword arguments. They survive markup
changes better than CSS:

```python
vibe.find(role="button", text="Sign in")
vibe.find(label="Email")
vibe.find(placeholder="Search...")
vibe.find(testid="checkout")
```

> **Nightly only.** A bare string is a plain-language description
> (`vibe.find("the Add to Cart button")`), and `css="..."` takes an exact
> CSS selector. In 26.8.21 a bare string is a CSS selector. The keyword
> forms above work in both.

## Let the AI drive

> **Nightly only.** See [Run and Check](../../run-and-check.md).

```python
result = vibe.run("open the contact page")
verdict = vibe.check("the page lists an email address")
```

## Custom binary

Set `VIBIUM_BIN_PATH` to use your own build of the binary:

```sh
export VIBIUM_BIN_PATH=/path/to/your/vibium
```

## Next

- [API Reference](api.md): every method, with its CLI and MCP equivalent.
- [Client Libraries](../index.md): the object model shared by all three languages.
- [Run and Check](../../run-and-check.md) and [Model Providers](../../ai-providers.md).
- [Troubleshooting](../../troubleshooting.md).
