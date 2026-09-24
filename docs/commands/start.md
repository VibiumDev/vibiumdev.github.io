---
title: vibium start
---

Start a browser session. Without arguments, launches a local browser.

## Synopsis

```
vibium start [url] [flags]
```

## Examples

```sh
vibium start
# Start with a local browser

vibium start --engine firefox
# Start with Firefox instead of Chrome

vibium start --engine firefox --channel beta
# Start with the installed Firefox beta instead of the release build

vibium start ws://remote:9515/session
# Connect to a remote browser

export VIBIUM_CONNECT_URL=wss://cloud.example.com/session
export VIBIUM_CONNECT_API_KEY=my-api-key
vibium start
# Connect using env vars

export VIBIUM_CONNECT_CAPS='{"vendor:options":{"someOption":"value"}}'
vibium start https://USER:KEY@grid.example.com/wd/hub
# Classic WebDriver endpoint: creates the session, then speaks BiDi
# Connected to https://grid.example.com/wd/hub (daemon pid 12345)
```
