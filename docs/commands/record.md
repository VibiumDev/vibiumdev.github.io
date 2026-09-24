---
title: vibium record
---

Record browser sessions (screenshots and snapshots).

## Synopsis

```
vibium record [flags]
vibium record [command]
```

## Subcommands

### vibium record chunk

Manage recording chunks.

```
vibium record chunk [flags]
vibium record chunk [command]
```

### vibium record chunk start

Start a new chunk within the current recording.

```
vibium record chunk start [flags]
```

#### Flags

```
    --name string    Name for the chunk
    --title string   Title shown in trace viewer
```

```sh
vibium record chunk start
# Start a new chunk (for splitting long recordings)

vibium record chunk start --name "part2" --title "Checkout Flow"
```

### vibium record chunk stop

Package current chunk into a ZIP file (recording stays active).

```
vibium record chunk stop [flags]
```

#### Flags

```
-o, --output string   Output file path (default: chunk.zip)
```

```sh
vibium record chunk stop
# Save chunk to chunk.zip

vibium record chunk stop -o part1.zip
```

### vibium record group

Manage recording groups.

```
vibium record group [flags]
vibium record group [command]
```

### vibium record group start

Start a named group in the recording.

```
vibium record group start <name> [flags]
```

```sh
vibium record group start "Login"
# Groups nest actions in the trace viewer
```

### vibium record group stop

End the current recording group.

```
vibium record group stop [flags]
```

```sh
vibium record group stop
```

### vibium record start

Start a recording.

```
vibium record start [flags]
```

#### Flags

```
    --bidi                  Record raw BiDi commands in the recording
    --format string         Screenshot format: jpeg or png (default "jpeg")
    --name string           Name for the recording (also seeds the default filename stem)
-o, --output string         Where the recording ZIP lands at stop (default: record-<timestamp>.zip)
    --quality float         JPEG quality 0.0-1.0 (ignored for png) (default 0.5)
    --screenshots           Capture screenshots after each action (default true)
    --snapshots             Capture HTML snapshots
    --sources               Include source information
    --title string          Title shown in trace viewer (defaults to name)
    --video                 Require video (omit: video when the engine supports it; =false: off)
    --video-fps int         Video frame rate (engine default if omitted)
    --video-remote string   On a remote connection, "keep" records anyway and leaves the video on the remote host
    --video-size string     Video dimensions as WxH, e.g. 1280x720 (default: viewport)
```

```sh
vibium record start
# Start recording with screenshots (default); video too when the
# engine supports it (Firefox 154+)

vibium record start --video -o record.zip
# Require video — fails with an explanatory error on Chrome
# Recording "record" started (video: on, ...), saving to record.zip

vibium record start --video --video-size 1280x720 --video-fps 30
# Explicit video dimensions (defaults follow the viewport)

vibium record start --video=false
# Record without video

vibium record start --screenshots=false
# Record without screenshots

vibium record start --snapshots
# Record with screenshots and HTML snapshots

vibium record start --format png
# Use PNG format instead of JPEG (larger files, lossless)

vibium record start --quality 0.1
# Lower JPEG quality for smaller recording files

vibium record start --title "Login Flow"
# Set a title shown in the trace viewer
```

### vibium record stop

Stop recording and save.

```
vibium record stop [flags]
```

#### Flags

```
-o, --output string   Output file path (default: record-<timestamp>.zip)
```

```sh
vibium record stop
# Saved record-20260808-094123.zip (23 steps, 14s video)

vibium record stop -o my-recording.zip
# Save to a custom path (overrides the path declared at start)
```

## Description

`record start` begins a recording. From that point on, Vibium captures a
screenshot at every step. `record stop` ends the recording and writes the
captured screenshots to `record.zip` in the current directory.

The resulting archive is useful for:

- Sharing a reproducible bug report.
- Auditing what an agent did during an autonomous run.
- Spot-checking the visual state of a session after the fact.

## Examples

```sh
vibium record start
vibium go https://example.com
vibium click @e1
vibium record stop
ls record.zip
```

## See also

- [`vibium screenshot`](screenshot.md) — one-off capture instead of a session.
