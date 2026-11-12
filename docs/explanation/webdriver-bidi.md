---
title: "WebDriver BiDi: The Standard Behind Vibium"
description: "Vibium is built on WebDriver BiDi, a W3C standard for browser automation."
editUrl: https://github.com/VibiumDev/vibium/edit/main/docs/explanation/webdriver-bidi.md
---

<!-- Imported from docs/explanation/webdriver-bidi.md in VibiumDev/vibium by scripts/import_upstream_docs.py. Edit it there. -->

Vibium is built on WebDriver BiDi, a W3C standard for browser automation. This doc explains what it is, where it came from, and why it matters.

## A Brief History

### Selenium and WebDriver (2004-present)

Browser automation started with Selenium in 2004. It injected JavaScript into pages to simulate user actions — clever, but limited by browser security.

WebDriver emerged as a cleaner approach: a separate process (the "driver") that controls the browser through a native API. Each browser vendor ships their own driver (chromedriver, geckodriver, etc.).

In 2018, WebDriver became a W3C standard. The protocol uses HTTP + JSON: send a POST request to click a button, get a JSON response. Simple, but strictly request-response: the client drives every interaction, and the browser can never push events unprompted.

### The CDP Era (2017-present)

Chrome DevTools Protocol (CDP) changed the game. It uses WebSockets instead of HTTP, enabling:

- **Bidirectional communication** — the browser can push events to the client
- **Real-time updates** — console logs, network requests, DOM changes as they happen
- **Low-level control** — things WebDriver couldn't do (network interception, coverage, etc.)

Puppeteer (2017) and Playwright (2020) were built on CDP. They're fast, powerful, and developer-friendly.

But CDP is Chrome-specific and internal. It changes without warning. Other browsers had to reverse-engineer or partially implement it. Not ideal for a standard.

### WebDriver BiDi (2021-present)

The W3C asked: what if we combined the best of both worlds?

- **Bidirectional** like CDP (WebSockets + JSON)
- **Standardized** like WebDriver (W3C spec, browser vendor buy-in)
- **Cross-browser** by design (Chrome, Firefox, Safari, Edge)

That's WebDriver BiDi.

## How It Works

```
┌─────────────┐                    ┌─────────────┐
│   Client    │◄───WebSocket──────►│   Browser   │
│  (Vibium)   │    (JSON msgs)     │             │
└─────────────┘                    └─────────────┘
```

Bidirectional communication over WebSocket. Messages are JSON:

```json
{"id": 1, "method": "browsingContext.navigate", "params": {"url": "https://example.com"}}
```

The browser responds:

```json
{"id": 1, "result": {"navigation": "123", "url": "https://example.com"}}
```

And the browser can push events without being asked:

```json
{"method": "log.entryAdded", "params": {"level": "error", "text": "Uncaught TypeError..."}}
```

## Current Status

WebDriver BiDi is shipping today:

| Browser | Status |
|---------|--------|
| Chrome/Chromium | Supported via chromedriver |
| Firefox | Native support (no separate driver) |
| Safari | In development |
| Edge | Supported (Chromium-based) |

Puppeteer added BiDi support in 2023. Selenium is integrating it. The ecosystem is converging.

## Why This Matters for Vibium

Building on WebDriver BiDi means:

1. **Standards-based.** We're building on a W3C standard, not proprietary protocols controlled by large corporations. CDP is controlled by Google. Playwright is controlled by Microsoft. WebDriver BiDi is governed by the W3C with input from all major browser vendors.

2. **Future-proof.** As browsers improve their BiDi support, Vibium gets better for free.

3. **Cross-browser potential.** Same API, multiple browsers (as support matures).

4. **Real-time events.** Console logs, network activity, DOM changes — pushed to agents as they happen.

The protocol handles the hard parts. Vibium focuses on making it accessible to AI agents and developers.

## Further Reading

- [WebDriver BiDi Spec](https://w3c.github.io/webdriver-bidi/) — the official W3C specification
- [Firefox Remote Protocols](https://firefox-source-docs.mozilla.org/remote/index.html) — Firefox's BiDi implementation
- [Firefox Developer Experience](https://fxdx.dev/category/remote-protocols/webdriver-bidi/) — Mozilla's BiDi blog updates
- [Puppeteer BiDi](https://pptr.dev/webdriver-bidi) — Puppeteer's BiDi integration
- [Selenium BiDi](https://www.selenium.dev/documentation/webdriver/bidi/) — Selenium's BiDi documentation
