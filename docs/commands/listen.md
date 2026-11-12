---
title: vibium listen
sidebar:
  badge: Nightly
---

Capture audio from a target and return a transcript.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium listen [flags]
```

## Flags

```
    --allow-silence     Return an empty transcript instead of failing when nothing is heard
    --duration int      Maximum milliseconds of capture, from the call (default 30000)
    --language string   BCP 47 tag (default en)
    --model string      Provider's model id
    --no-transcribe     Capture without a transcript; speech onset and reply latency are still reported
-o, --output string     Also save the captured audio as a WAV file
    --provider string   Speech-to-text provider or preset (default: from the environment)
    --silence int       Milliseconds of trailing silence that end the reply; 0 turns endpointing off (default 1000)
    --target string     session, local, or a path ending in .wav (default: the session if one is open, else local)
    --timeout int       Milliseconds to wait for speech to start, from the call (default 10000)
```

## Examples

```sh
vibium listen
# Come here, Watson.

vibium listen --timeout 5000 --json
# {"ok":true,"result":{"text":"Come here, Watson.","speech":true,"onsetMs":640,"speechEndMs":2010,"latencyMs":640,"stoppedBy":"silence",...}}

vibium listen --target reply.wav --silence 0
# Transcribes the whole file.

vibium listen --silence 0 --duration 5000 -o five-seconds.wav
# Captures exactly five seconds and saves them.

vibium listen --no-transcribe -o reply.wav
# Heard 2.1 s of speech after 640 ms (reply.wav)
# Saves the reply without transcribing it. Transcribe it later:
vibium listen --target reply.wav
```
