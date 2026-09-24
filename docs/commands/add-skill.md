---
title: vibium add-skill
---

Install a Vibium skill for Grok and Claude Code.

## Synopsis

```
vibium add-skill [browser|check] [flags]
```

## Flags

```
    --agent string   Install for claude, grok, all, or auto (agents already present) (default "auto")
    --stdout         Print skill content to stdout instead of installing
```

New in nightly (not yet in the npm release): `--agent`

## Examples

```sh
vibium add-skill
# Installs for each agent already present (~/.claude, ~/.grok, or $GROK_HOME)

vibium add-skill check --agent all
# Installs the check skill for both agents, creating their directories

vibium add-skill --agent grok
# Grok only ($GROK_HOME/skills or ~/.grok/skills)

vibium add-skill check --stdout
# Print skill content to stdout
```
