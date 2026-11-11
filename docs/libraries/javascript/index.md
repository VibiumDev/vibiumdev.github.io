---
title: JavaScript and TypeScript
description: Install the Vibium JavaScript client, run a first script, and choose between the async and sync APIs.
---

The `vibium` npm package drives a real browser from Node.js. It ships
TypeScript types and bundles the `vibium` binary for your platform.

## Requirements

- Node.js 18 or newer
- Linux x64/arm64, macOS x64/arm64, or Windows x64

## Install

```sh
npm install vibium
```

Chrome for Testing downloads the first time a browser starts. To fetch it
ahead of time, run `npx vibium install`.

## First script

Save this as `hello.mjs`:

```javascript
import { writeFileSync } from 'node:fs'
import { browser } from 'vibium'

// Launch a browser. The window is visible by default.
const bro = await browser.start()
const vibe = await bro.page()

await vibe.go('https://example.com')
writeFileSync('screenshot.png', await vibe.screenshot())

const link = await vibe.find({ role: 'link' })
console.log('Found link:', await link.text())
await link.click()

await bro.stop()
```

Run it:

```sh
node hello.mjs
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
| `vibe.find({ role: 'link' })` | Finds an element by its accessible role |
| `link.click()` | Clicks the element |
| `bro.stop()` | Closes the browser |

## Sync API

The default import is async. `vibium/sync` exposes the same API without
`await`, which suits short scripts and the Node REPL:

```javascript
const { browser } = require('vibium/sync')

const bro = browser.start()
const vibe = bro.page()
vibe.go('https://example.com')
console.log(vibe.find({ role: 'link' }).text())
bro.stop()
```

## Options

Hide the browser window:

```javascript
const bro = await browser.start({ headless: true })
```

Launch Firefox instead of Chrome:

```javascript
import { firefox, browser } from 'vibium'

const bro = await firefox.start()
// same as: await browser.start({ engine: 'firefox' })
```

See [Using Firefox](../../using-firefox.md) for engine details.

## Finding elements

`find` takes semantic locators. They survive markup changes better than CSS:

```javascript
await vibe.find({ role: 'button', text: 'Sign in' })
await vibe.find({ label: 'Email' })
await vibe.find({ placeholder: 'Search...' })
await vibe.find({ testid: 'checkout' })
```

> **Nightly only.** A bare string is a plain-language description
> (`vibe.find('the Add to Cart button')`), and `{ css: '...' }` takes an
> exact CSS selector. In 26.8.21 a bare string is a CSS selector. The
> object forms above work in both.

## Let the AI drive

> **Nightly only.** See [Run and Check](../../run-and-check.md).

```javascript
const result = await vibe.run('open the contact page')
const verdict = await vibe.check('the page lists an email address')
```

## Next

- [API Reference](api.md): every method, with its CLI and MCP equivalent.
- [Client Libraries](../index.md): the object model shared by all three languages.
- [Run and Check](../../run-and-check.md) and [Model Providers](../../ai-providers.md).
- [Troubleshooting](../../troubleshooting.md).
