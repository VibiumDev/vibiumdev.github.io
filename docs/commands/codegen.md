---
title: vibium codegen
---

Generate a runnable script that replays a recording's action stream.

## Synopsis

```
vibium codegen -i <recording.zip> [flags]
```

## Flags

```
-i, --input string      Recording zip to read (required)
-l, --language string   Script language: javascript or python (default "javascript")
-o, --output string     Save the script as a new file instead of printing it
```

## Examples

```sh
vibium codegen -i record.zip
# Prints a JavaScript replay script to stdout:
#   import { browser } from 'vibium';
#   ...
#   await vibe.go('https://var.parts');
#   await vibe.find({ text: 'Vibium Battery Pack' }).click();
vibium codegen -i record.zip --language python -o replay.py
# Saves the Python version of the script as a new file.
```
