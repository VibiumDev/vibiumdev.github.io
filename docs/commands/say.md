---
title: vibium say
sidebar:
  badge: Nightly
---

Turn text into speech and play it into a target.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium say "<text>" | say --file <clip.wav> [flags]
```

## Flags

```
    --cache-dir string   Where rendered audio is kept
    --file string        A WAV file to play as it is, in place of text
    --language string    BCP 47 tag, for providers that take one
    --model string       Provider's model id
    --no-cache           Render again and replace the cached audio
    --provider string    Text-to-speech provider or preset (default: from the environment)
    --speed float        Speaking rate multiplier, where the provider supports it (default 1)
    --target string      session, local, or a path ending in .wav (default: the session if one is open, else local)
    --voice string       Provider's voice id
```

## Examples

```sh
vibium say "Come here, Watson"
# Said "Come here, Watson" (1.4 s, openai gpt-4o-mini-tts cedar)

vibium say "Come here, Watson" --target watson.wav
# Wrote watson.wav (1.4 s, openai gpt-4o-mini-tts cedar, cached)

echo "What time is it?" | vibium say - --target local
# Reads the text from stdin.

VIBIUM_PIPER_URL=http://127.0.0.1:5000 vibium say "Come here, Watson"
# Said "Come here, Watson" (1.2 s, piper-server)
# Speaks through a Piper server you started, which keeps its voice loaded.

vibium say -- "-5 degrees"
# Text that starts with a dash goes after --.

vibium say --file question.wav
# Played question.wav (2.3 s)
# Plays a recording as it is. No speech engine or key is needed.
```
