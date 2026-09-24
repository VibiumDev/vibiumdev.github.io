---
title: vibium config
sidebar:
  badge: Nightly
---

Manage Vibium settings files.

## Synopsis

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium config [command]
```

## Subcommands

### vibium config init

Write a commented settings file to the Vibium config directory.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium config init [ai|cloud|all] [flags]
```

#### Flags

```
    --force    Overwrite an existing file, keeping a .bak copy
    --stdout   Print the template instead of writing it
```

```sh
vibium config init
# Wrote ~/.config/vibium/ai.env (0600); next vibium command loads empty AI vars from it

vibium config init cloud
# Wrote ~/.config/vibium/cloud-browser.env (0600)

vibium config init all --force
# Overwrites both, keeping a .bak of each

vibium config init ai --stdout
# Print the template instead of writing it
```
