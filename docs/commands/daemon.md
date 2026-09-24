---
title: vibium daemon
---

Manage the vibium daemon (background browser process).

## Synopsis

```
vibium daemon [flags]
vibium daemon [command]
```

## Subcommands

### vibium daemon start

Start the vibium daemon.

```
vibium daemon start [flags]
```

#### Flags

```
    --connect string               Connect to a remote BiDi WebSocket URL instead of launching a local browser
    --connect-caps string          Extra alwaysMatch capabilities for classic WebDriver endpoints (JSON object)
    --connect-header stringArray   HTTP header for WebSocket connect (repeatable, format: "Key: Value")
    --foreground                   Run daemon in foreground (for debugging)
    --idle-timeout duration        Shutdown after this duration of inactivity (0 to disable) (default 30m0s)
```

New in nightly (not yet in the npm release): `--connect-caps`

```sh
vibium daemon start
# Starts daemon in background

vibium daemon start --foreground
# Starts daemon in foreground (for debugging)

vibium daemon start --idle-timeout 30m
# Auto-shutdown after 30 minutes of inactivity

vibium daemon start --connect ws://remote:9515/session
# Connect to a remote browser instead of launching a local one

vibium daemon start --connect https://USER:KEY@grid.example.com/wd/hub \
  --connect-caps '{"vendor:options":{"someOption":"value"}}'
# Classic WebDriver endpoint (Selenium Grid, cloud grid): vibium creates
# a session with webSocketUrl:true and connects to the BiDi URL it returns

vibium --session projA daemon start
# Isolated session "projA": own daemon, own browser, socket
# vibium-projA.sock; VIBIUM_SESSION=projA does the same

vibium daemon start --json
# {"ok":true,"result":{"pid":79311,"running":true,"started":true}}
```

### vibium daemon status

Show daemon status.

```
vibium daemon status [flags]
```

### vibium daemon stop

Stop the vibium daemon.

```
vibium daemon stop [flags]
```

```sh
vibium daemon stop
# Daemon stopped.

vibium daemon stop --json
# {"ok":true,"result":{"running":false,"stopped":true}}
```
