---
title: vibium dialog
---

Handle browser dialogs (alert, confirm, prompt).

## Synopsis

```
vibium dialog [flags]
vibium dialog [command]
```

## Subcommands

### vibium dialog accept

Accept a dialog (optionally with prompt text).

```
vibium dialog accept [text] [flags]
```

```sh
vibium dialog accept
# Accept an alert or confirm dialog

vibium dialog accept "my input"
# Accept a prompt dialog with text
```

### vibium dialog dismiss

Dismiss a dialog.

```
vibium dialog dismiss [flags]
```

```sh
vibium dialog dismiss
# Dismiss/cancel a dialog
```
