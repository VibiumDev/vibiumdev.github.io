---
title: "Process Cleanup"
description: "When Vibium launches a browser session, it creates this process hierarchy:"
editUrl: https://github.com/VibiumDev/vibium/edit/main/docs/explanation/process-cleanup.md
---

<!-- Imported from docs/explanation/process-cleanup.md in VibiumDev/vibium by scripts/import_upstream_docs.py. Edit it there. -->

## Process Tree

When Vibium launches a browser session, it creates this process hierarchy:

```
vibium (Go binary)
  └── chromedriver
        └── Chrome for Testing (main browser process)
              ├── chrome_crashpad_handler (crash reporting)
              ├── GPU helper
              ├── Network helper
              ├── Storage helper
              ├── Renderer helper (one per tab/frame)
              └── ...more helpers
```

A single browser session spawns 8-12 processes.

## The Problem

When we kill chromedriver, its children (Chrome + helpers) get **reparented to PID 1** (launchd on macOS, init on Linux) before we can kill them. The process tree disintegrates mid-cleanup, leaving orphaned "zombie" processes.

```
Before kill:                    After chromedriver dies:
chromedriver                    (gone)
  └── Chrome                    Chrome (parent = 1, orphaned!)
        └── GPU helper            └── GPU helper
        └── Renderer              └── Renderer
```

### Why not kill Chrome first?

We try - `DELETE /session` tells chromedriver to quit Chrome gracefully. But this can fail:

- **Ctrl+C** - Signal kills chromedriver before DELETE completes
- **Timeout** - DELETE request fails or Chrome doesn't exit fast enough
- **Race** - Chromedriver dies before Chrome fully shuts down

## The Solution

Our cleanup strategy in `launcher.go:Close()`:

1. **DELETE /session** - Ask chromedriver to quit Chrome gracefully (best effort, skipped on Windows)
2. **Kill process tree** - Recursively find all descendants using `pgrep -P`, then kill deepest-first
3. **Kill orphans** - Sweep for any Chrome/chromedriver processes with parent PID 1 and kill them
4. **Clean up temp dirs** - Remove orphaned Chrome temp directories from `os.TempDir()`

```go
func killProcessTree(pid int) {
    descendants := getDescendants(pid)  // recursive pgrep -P
    // Kill children first (deepest first)
    for i := len(descendants) - 1; i >= 0; i-- {
        killByPid(descendants[i])
    }
    killByPid(pid)

    // Sweep for orphans that escaped
    KillOrphanedChromeProcesses()
}
```

## What if vibium itself dies?

| Scenario | What happens |
|----------|--------------|
| Normal exit | `Close()` cleans up children |
| Ctrl+C | Signal handler calls `KillAll()` |
| `kill -9` | Orphans created, nothing we can do |

For `kill -9`, the orphan cleanup in the *next* session's `Close()` will find and kill them. Or use `make double-tap`.

The vibium binary itself doesn't leave zombies - it's just a Go process that exits cleanly. The issue is its children (chromedriver/Chrome) escaping cleanup.

## Manual Cleanup

If zombie processes accumulate during development:

```bash
make double-tap
```

This kills all Chrome for Testing and chromedriver processes.

## Debugging

Check for zombie processes:

```bash
pgrep -lf 'Chrome for Testing'
pgrep -lf chromedriver
```

Check parent PIDs to see if they're orphaned:

```bash
ps -o pid,ppid,comm -p $(pgrep -f 'Chrome for Testing')
```

Orphaned processes will have `PPID = 1`.
