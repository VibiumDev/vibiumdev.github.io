---
title: vibium pipe
---

Start vibium in pipe mode where protocol messages are exchanged.

## Synopsis

```
vibium pipe [flags]
```

## Flags

```
    --connect string               Connect to a remote BiDi WebSocket URL instead of launching a local browser
    --connect-caps string          Extra alwaysMatch capabilities for classic WebDriver endpoints (JSON object)
    --connect-header stringArray   HTTP header for WebSocket connect (repeatable, format: "Key: Value")
    --no-browser                   Start the existing pipe runtime for read-only archive commands without installing or launching a browser
```

New in nightly (not yet in the npm release): `--connect-caps`, `--no-browser`

## Examples

```sh
{ echo '{"id":1,"method":"vibium:browser.page","params":{}}'; cat; } | vibium pipe --headless
# Drive the protocol by hand; Ctrl-C when done. cat holds stdin open past
# the browser launch. A bare echo closes it first and the command comes
# back {"type":"error","message":"connection closed"}.

# Read-only archive commands, no browser startup
vibium pipe --no-browser

# Connect to a remote browser
vibium pipe --connect ws://remote:9515

# Connect with auth header
vibium pipe --connect wss://cloud.example.com/bidi --connect-header "Authorization: Bearer token"

# Classic WebDriver endpoint (Selenium Grid, cloud grid): vibium creates
# a session with webSocketUrl:true and connects to the BiDi URL it returns
vibium pipe --connect https://USER:KEY@grid.example.com/wd/hub \
  --connect-caps '{"vendor:options":{"someOption":"value"}}'
```
