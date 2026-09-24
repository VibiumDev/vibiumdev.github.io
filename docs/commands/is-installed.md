---
title: vibium is-installed
---

Check if the selected browser is installed (exit 0 = yes, exit 1 = no).

## Synopsis

```
vibium is-installed [flags]
```

## Examples

```sh
vibium is-installed && echo yes
# yes

vibium is-installed --json
# {"ok":true,"result":{"engine":"chrome","installed":true}}
```
