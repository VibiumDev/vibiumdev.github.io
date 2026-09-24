---
title: Recording
---

`vibium record` captures a session — a trace of every action, screenshots per
step, optionally HTML snapshots, and (on Firefox) a native video track — into
a single zip you can share, attach to a bug report, or play back in the
[Vibium Record Player](https://player.vibium.dev/).

## Record a session

```sh
vibium record start
vibium go https://example.com
vibium find text "More information"
vibium click @e1
vibium record stop   # writes record.zip
```

`record start` accepts `-o` to name the output, `--screenshots=false`,
`--snapshots` (HTML snapshots), `--format png`, and `--quality` to trade
size against fidelity.

## Video

Recordings include a video track whenever the engine supports it — the
browser itself encodes the viewport to WebM via the WebDriver BiDi
screencast command, nothing extra to install:

```sh
vibium record start --video --video-size 1280x720 --video-fps 30
```

Video requires **Firefox 154 or newer** (a plain `--engine firefox` is
enough; Vibium installs it). Chrome has not implemented the BiDi screencast
command yet: with `--video` omitted, a Chrome recording simply proceeds
without a video track; explicit `--video` fails with an error saying so.
See [Using Firefox](using-firefox.md).

## Groups and chunks

Longer recordings can be structured:

- `vibium record group start "checkout"` / `record group stop` label a
  logical phase inside the recording.
- `vibium record chunk start` / `record chunk stop` split the output into
  multiple zips, so a long session doesn't produce one huge file.

## Privacy

Recording metadata is redacted before it is written — API keys (including
provider keys used by [Run and Check](run-and-check.md)) never enter the
zip.

## From the clients

Every client exposes the same controls via `recording.start()` /
`recording.stop()`, including the `video` option. [Run and
Check](run-and-check.md) accept `-o` to save their whole AI-driven session
as a recording in the same format.
