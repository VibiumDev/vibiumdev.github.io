---
title: Command Reference
sidebar:
  order: 0
---

Every command the `vibium` binary exposes, one page per command. This
reference is generated from the binary itself, so it always matches what
`vibium --help` reports. Start with the day-to-day loop —
[`go`](go.md), [`map`](map.md), [`find`](find.md), [`click`](click.md),
[`fill`](fill.md), [`text`](text.md), [`screenshot`](screenshot.md) — or
hand the whole task to a model with [`run`](run.md) and verify it with
[`check`](check.md).

| Command | Description |
| ------- | ----------- |
| [`vibium a11y-tree`](a11y-tree.md) | Get the accessibility tree of the current page |
| [`vibium add-skill`](add-skill.md) | Install a Vibium skill for Grok and Claude Code |
| [`vibium attr`](attr.md) | Get an HTML attribute value from an element |
| [`vibium back`](back.md) | Navigate back in browser history |
| [`vibium check`](check.md) | Check a claim in a live browser or an existing recording with an independent model. |
| [`vibium click`](click.md) | Click an element (optionally navigate to URL first) |
| [`vibium config`](config.md) **(nightly)** | Manage Vibium settings files |
| [`vibium content`](content.md) | Replace the page HTML content |
| [`vibium cookies`](cookies.md) | Manage browser cookies |
| [`vibium count`](count.md) | Count matching elements |
| [`vibium daemon`](daemon.md) | Manage the vibium daemon (background browser process) |
| [`vibium dblclick`](dblclick.md) | Double-click an element |
| [`vibium dialog`](dialog.md) | Handle browser dialogs (alert, confirm, prompt) |
| [`vibium diff`](diff.md) | Compare current state vs previous |
| [`vibium download`](download.md) | Manage browser downloads |
| [`vibium drag`](drag.md) | Drag from one element to another |
| [`vibium eval`](eval.md) | Evaluate a JavaScript expression (optionally navigate to URL first) |
| [`vibium fill`](fill.md) | Clear an input field and type new text |
| [`vibium find`](find.md) | Find elements by CSS selector or semantic locator |
| [`vibium focus`](focus.md) | Focus an element |
| [`vibium forward`](forward.md) | Navigate forward in browser history |
| [`vibium frame`](frame.md) | Find a frame by name or URL substring |
| [`vibium frames`](frames.md) | List all child frames (iframes) on the page |
| [`vibium geolocation`](geolocation.md) | Override the browser geolocation |
| [`vibium go`](go.md) | Go to a URL and print page info |
| [`vibium highlight`](highlight.md) | Highlight an element with a red outline for 3 seconds |
| [`vibium hover`](hover.md) | Hover over an element by CSS selector |
| [`vibium html`](html.md) | Get HTML content of the page or an element |
| [`vibium install`](install.md) | Download the selected browser (Chrome for Testing by default) |
| [`vibium is`](is.md) | Check element state (visible, enabled, set, actionable) |
| [`vibium is-installed`](is-installed.md) | Check if the selected browser is installed (exit 0 = yes, exit 1 = no) |
| [`vibium keys`](keys.md) | Press a key or key combination |
| [`vibium map`](map.md) | Map interactive page elements with @refs |
| [`vibium mcp`](mcp.md) | Start the Model Context Protocol (MCP) server. |
| [`vibium media`](media.md) | Override CSS media features |
| [`vibium mouse`](mouse.md) | Mouse control (click, move, down, up) |
| [`vibium page`](page.md) | Manage browser pages (new, close, switch) |
| [`vibium pages`](pages.md) | List all open browser pages |
| [`vibium paths`](paths.md) | Print browser and cache paths for the selected engine |
| [`vibium pdf`](pdf.md) | Save page as PDF |
| [`vibium pipe`](pipe.md) | Start vibium in pipe mode where protocol messages are exchanged |
| [`vibium press`](press.md) | Press a key on a specific element or the focused element |
| [`vibium ready`](ready.md) **(nightly)** | Check the selected local browser executable files, then test AI when configured. No browser or driver is launched. |
| [`vibium record`](record.md) | Record browser sessions (screenshots and snapshots) |
| [`vibium reload`](reload.md) | Reload the current page |
| [`vibium run`](run.md) **(nightly)** | Accomplish a live browser goal using VIBIUM_AI_* configuration. |
| [`vibium screenshot`](screenshot.md) | Capture a screenshot (optionally navigate to URL first) |
| [`vibium scroll`](scroll.md) | Scroll the page or an element |
| [`vibium select`](select.md) | Select an option in a <select> element |
| [`vibium serve`](serve.md) | Start WebSocket proxy server for browser automation |
| [`vibium set`](set.md) **(nightly)** | Check a checkbox or radio button |
| [`vibium setup`](setup.md) **(nightly)** | Interactive setup for AI settings, agent skills, and the local browser. |
| [`vibium sleep`](sleep.md) | Pause execution for a number of milliseconds |
| [`vibium start`](start.md) | Start a browser session. Without arguments, launches a local browser. |
| [`vibium stop`](stop.md) | Stop the browser session |
| [`vibium storage`](storage.md) | Export or restore browser state (cookies, localStorage, sessionStorage) |
| [`vibium text`](text.md) | Get text content of the page or an element |
| [`vibium title`](title.md) | Get the current page title |
| [`vibium type`](type.md) | Type text into an element (optionally navigate to URL first) |
| [`vibium unset`](unset.md) **(nightly)** | Uncheck a checkbox |
| [`vibium upload`](upload.md) | Set files on an input[type=file] element |
| [`vibium url`](url.md) | Get the current page URL |
| [`vibium value`](value.md) | Get the current value of a form element |
| [`vibium version`](version.md) | Print the version number |
| [`vibium viewport`](viewport.md) | Get or set the browser viewport size |
| [`vibium wait`](wait.md) | Wait for an element, URL, text, page load, or JS condition |
| [`vibium window`](window.md) | Get or set the OS browser window size, position, or state |

Commands marked **(nightly)** are not yet in the latest npm release; see [What's in Nightly](../nightly.md).

## Global flags

Every command accepts these flags in addition to its own:

```
    --channel string   Engine release channel to install and run (env: VIBIUM_ENGINE_CHANNEL); firefox: release (default) or beta; chrome: stable (default), beta, dev, or canary
    --engine string    Browser engine to launch: chrome or firefox (env: VIBIUM_ENGINE) (default "chrome")
    --headless         Hide browser window (visible by default)
    --json             Output as JSON
    --session string   Named daemon session for isolated concurrent use (env: VIBIUM_SESSION)
-v, --verbose          Enable debug logging
    --version          version for vibium
```
