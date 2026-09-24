---
title: vibium is
---

Check element state (visible, enabled, set, actionable).

## Synopsis

```
vibium is [flags]
vibium is [command]
```

## Subcommands

### vibium is actionable

Check actionability of an element (Visible, Stable, ReceivesEvents, Enabled, Editable).

```
vibium is actionable [url] [selector] [flags]
```

```sh
vibium is actionable "a"
# Output:
# Checking actionability for selector: a
# ✓ Visible: true
# ✓ Stable: true
# ✓ ReceivesEvents: true
# ✓ Enabled: true
# ✗ Editable: false

vibium is actionable https://example.com "a"
# Navigate first, then check
```

### vibium is enabled

Check if an element is enabled.

```
vibium is enabled [selector] [flags]
```

#### Flags

```
    --fail   Exit non-zero when the answer is false
```

```sh
vibium is enabled "button[type=submit]"
# Prints true or false
```

### vibium is set

Check if a checkbox or radio is checked.

> **Nightly only.** This command is in the nightly builds but not yet in the latest npm release. See [What's in Nightly](../nightly.md).

```
vibium is set [selector] [flags]
```

#### Flags

```
    --fail   Exit non-zero when the answer is false
```

```sh
vibium is set "input[type=checkbox]"
# Prints true or false
```

### vibium is visible

Check if an element is visible on the page.

```
vibium is visible [selector] [flags]
```

#### Flags

```
    --fail   Exit non-zero when the answer is false
```

```sh
vibium is visible "h1"
# Prints true or false
```
