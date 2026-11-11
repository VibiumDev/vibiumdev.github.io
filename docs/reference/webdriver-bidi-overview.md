---
title: "WebDriver BiDi Protocol Reference"
description: "All module.method names from the WebDriver BiDi spec (editor's draft)."
editUrl: https://github.com/VibiumDev/vibium/edit/main/docs/reference/webdriver-bidi-overview.md
---

<!-- Imported from docs/reference/webdriver-bidi-overview.md in VibiumDev/vibium by scripts/import_upstream_docs.py. Edit it there. -->

All `module.method` names from the [WebDriver BiDi spec](https://w3c.github.io/webdriver-bidi/) (editor's draft).

---

## Commands

### session

| Method | Description |
|--------|-------------|
| `session.status` | Returns whether the remote end can create new sessions |
| `session.new` | Creates a new BiDi session |
| `session.end` | Ends the current session |
| `session.subscribe` | Enables events globally or for specific navigables |
| `session.unsubscribe` | Disables events globally or for specific navigables |

### browser

| Method | Description |
|--------|-------------|
| `browser.close` | Terminates all WebDriver sessions and cleans up the browser |
| `browser.createUserContext` | Creates a new user context (profile/container) |
| `browser.getClientWindows` | Returns a list of client windows |
| `browser.getUserContexts` | Returns a list of user contexts |
| `browser.removeUserContext` | Closes a user context and all its navigables without beforeunload |
| `browser.setClientWindowState` | Sets the dimensions/state of a client window |
| `browser.setDownloadBehavior` | Configures download behavior (allow/deny, destination folder) |

### browsingContext

| Method | Description |
|--------|-------------|
| `browsingContext.activate` | Activates and focuses a top-level traversable |
| `browsingContext.captureScreenshot` | Captures a screenshot, returned as a Base64-encoded string |
| `browsingContext.close` | Closes a top-level traversable |
| `browsingContext.create` | Creates a new navigable in a new tab or window |
| `browsingContext.getTree` | Returns the tree of all descendant navigables |
| `browsingContext.handleUserPrompt` | Closes an open prompt (alert/confirm/prompt) |
| `browsingContext.locateNodes` | Returns all nodes matching a locator (CSS, XPath, accessibility, etc.) |
| `browsingContext.navigate` | Navigates a navigable to a URL |
| `browsingContext.print` | Prints a document to PDF, returned as a Base64-encoded string |
| `browsingContext.reload` | Reloads a navigable |
| `browsingContext.setBypassCSP` | Bypasses Content Security Policy enforcement |
| `browsingContext.setViewport` | Sets viewport width, height, and device pixel ratio |
| `browsingContext.traverseHistory` | Traverses session history by a delta (back/forward) |

### emulation

| Method | Description |
|--------|-------------|
| `emulation.setForcedColorsModeThemeOverride` | Overrides forced-colors mode theming (light/dark) |
| `emulation.setGeolocationOverride` | Overrides geolocation coordinates or simulates position error |
| `emulation.setLocaleOverride` | Overrides locale for navigables or user contexts |
| `emulation.setNetworkConditions` | Emulates network conditions (e.g. offline) |
| `emulation.setScreenOrientationOverride` | Emulates screen orientation (portrait/landscape) |
| `emulation.setScreenSettingsOverride` | Emulates screen area dimensions |
| `emulation.setScriptingEnabled` | Emulates disabled JavaScript on web pages |
| `emulation.setScrollbarTypeOverride` | Overrides scrollbar type |
| `emulation.setTimezoneOverride` | Overrides timezone |
| `emulation.setTouchOverride` | Emulates touch input support |
| `emulation.setUserAgentOverride` | Overrides User-Agent per navigable, user context, or globally |

### network

| Method | Description |
|--------|-------------|
| `network.addDataCollector` | Adds a network data collector |
| `network.addIntercept` | Adds a network intercept for request/response phases |
| `network.continueRequest` | Continues a request blocked by an intercept |
| `network.continueResponse` | Continues a response blocked by an intercept (can modify status/headers) |
| `network.continueWithAuth` | Continues a response blocked at the authRequired phase |
| `network.disownData` | Releases collected network data for a given collector |
| `network.failRequest` | Fails a fetch blocked by an intercept |
| `network.getData` | Retrieves collected network data if available |
| `network.provideResponse` | Provides a complete synthetic response for an intercepted request |
| `network.removeDataCollector` | Removes a network data collector |
| `network.removeIntercept` | Removes a network intercept |
| `network.setCacheBehavior` | Configures cache behavior (default/bypass) |
| `network.setExtraHeaders` | Sets extra headers that extend or overwrite request headers |

### script

| Method | Description |
|--------|-------------|
| `script.addPreloadScript` | Adds a script that runs before page scripts on new documents |
| `script.callFunction` | Calls a function with arguments in a given realm |
| `script.disown` | Releases ownership of remote object handles |
| `script.evaluate` | Evaluates an expression in a given realm |
| `script.getRealms` | Returns all realms, optionally filtered by type or navigable |
| `script.removePreloadScript` | Removes a preload script |

### input

| Method | Description |
|--------|-------------|
| `input.performActions` | Performs a sequence of user input actions |
| `input.releaseActions` | Resets input state for the current session |
| `input.setFiles` | Sets the files on an `<input type="file">` element |

### storage

| Method | Description |
|--------|-------------|
| `storage.deleteCookies` | Removes cookies matching the given parameters |
| `storage.getCookies` | Retrieves cookies matching the given parameters |
| `storage.setCookie` | Creates or replaces a cookie in a cookie store |

### webExtension

| Method | Description |
|--------|-------------|
| `webExtension.install` | Installs a web extension |
| `webExtension.uninstall` | Uninstalls a web extension |

---

## Events

### browsingContext

| Event | Description |
|-------|-------------|
| `browsingContext.contextCreated` | A navigable was created |
| `browsingContext.contextDestroyed` | A navigable was destroyed |
| `browsingContext.domContentLoaded` | DOMContentLoaded fired in a navigable |
| `browsingContext.downloadEnd` | A download completed or was canceled |
| `browsingContext.downloadWillBegin` | A download is about to start |
| `browsingContext.fragmentNavigated` | A fragment navigation occurred |
| `browsingContext.historyUpdated` | History was updated (e.g. pushState/replaceState) |
| `browsingContext.load` | The load event fired in a navigable |
| `browsingContext.navigationAborted` | A navigation was aborted |
| `browsingContext.navigationCommitted` | A navigation was committed |
| `browsingContext.navigationFailed` | A navigation failed |
| `browsingContext.navigationStarted` | A navigation started |
| `browsingContext.userPromptClosed` | A user prompt was closed |
| `browsingContext.userPromptOpened` | A user prompt was opened |

### input

| Event | Description |
|-------|-------------|
| `input.fileDialogOpened` | A file picker dialog was opened |

### log

| Event | Description |
|-------|-------------|
| `log.entryAdded` | A log entry was added (console, JS error, etc.) |

### network

| Event | Description |
|-------|-------------|
| `network.authRequired` | Authentication was required for a request |
| `network.beforeRequestSent` | A request is about to be sent |
| `network.fetchError` | A fetch encountered a network error |
| `network.responseCompleted` | A response completed |
| `network.responseStarted` | A response started arriving |

### script

| Event | Description |
|-------|-------------|
| `script.message` | A message was sent via a BiDi channel |
| `script.realmCreated` | A new realm was created |
| `script.realmDestroyed` | A realm was destroyed |
