---
title: vibium paths
---

Print browser and cache paths for the selected engine.

## Synopsis

```
vibium paths [flags]
```

## Examples

```sh
vibium paths
# Cache directory: ~/Library/Caches/vibium
# Chrome: .../Google Chrome for Testing
# Chromedriver: .../chromedriver

vibium --engine firefox paths
# Cache directory: ~/Library/Caches/vibium
# Firefox: .../Firefox.app/Contents/MacOS/firefox

vibium paths --json
# {"ok":true,"result":{"engine":"chrome","cacheDir":"...","chrome":"...","chromedriver":"..."}}
```
