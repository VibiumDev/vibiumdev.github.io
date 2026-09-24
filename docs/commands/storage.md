---
title: vibium storage
---

Export or restore browser state (cookies, localStorage, sessionStorage).

## Synopsis

```
vibium storage [flags]
vibium storage [command]
```

## Flags

```
-o, --output string   Output file path
```

## Subcommands

### vibium storage restore

Restore browser state from a JSON file.

```
vibium storage restore [path] [flags]
```

```sh
vibium storage restore state.json
# Restore cookies and storage from saved state
```

## Examples

```sh
vibium storage
# Print state as JSON

vibium storage -o state.json
# Save state to file
```
