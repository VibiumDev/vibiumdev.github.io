---
title: vibium find
---

Find elements by CSS selector or semantic locator.

## Synopsis

```
vibium find [selector] [flags]
vibium find [command]
```

## Flags

```
    --all               Find all matching elements
    --limit int         Maximum number of elements to return (with --all) (default 10)
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

## Subcommands

### vibium find alt

Find element by alt attribute.

```
vibium find alt [alt] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find alt "Logo"
```

### vibium find label

Find input by associated label text.

```
vibium find label [label] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find label "Email"
# → @e1 [input type="email"] placeholder="Email"
```

### vibium find placeholder

Find element by placeholder attribute.

```
vibium find placeholder [placeholder] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find placeholder "Search..."
# → @e1 [input] placeholder="Search..."
```

### vibium find role

Find element by ARIA role.

```
vibium find role [role] [flags]
```

#### Flags

```
    --name string       Accessible name filter
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find role button
# → @e1 [button] "Submit"

vibium find role heading --name "Example"
# Find heading with accessible name "Example"
```

### vibium find testid

Find element by data-testid attribute.

```
vibium find testid [testid] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find testid "submit-btn"
# → @e1 [button] data-testid="submit-btn"
```

### vibium find text

Find element by text content.

```
vibium find text [text] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find text "Sign In"
# → @e1 [button] "Sign In"
```

### vibium find title

Find element by title attribute.

```
vibium find title [title] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find title "Close"
```

### vibium find xpath

Find element by XPath expression.

```
vibium find xpath [expression] [flags]
```

#### Flags

```
    --timeout timeout   Max time to wait, e.g. 5s or 5000 (bare number = milliseconds) (default 30s)
```

```sh
vibium find xpath "//div[@class='main']"
# → @e1 [div.main] ...
```

## Description

`find` matches elements the way a human would describe them, returning one or
more `@eN` references you can pass to interaction commands.

| Variant                              | Matches                                                                 |
| ------------------------------------ | ----------------------------------------------------------------------- |
| `vibium find text "<text>"`          | Elements whose visible text contains `<text>`.                          |
| `vibium find label "<label>"`        | Form fields whose `<label>` is `<label>`.                               |
| `vibium find placeholder "<text>"`   | Inputs with that placeholder.                                           |
| `vibium find role <role>`            | Elements with the given ARIA role (`button`, `searchbox`, `link`, …).   |

Each match is printed in the same form as [`vibium map`](map.md): a line per
element with its `@eN` reference, role, and a short description.

## Examples

```sh
vibium find text "Sign in"
vibium find label "Email"
vibium find placeholder "Search..."
vibium find role button
```

Typical workflow — find, then act on the reference:

```sh
$ vibium find label "Email"
@e2  input  label="Email"

$ vibium fill @e2 "alice@example.com"
```

## See also

- [`vibium map`](map.md) — list every element instead of finding one.
- [`vibium click`](click.md), [`vibium fill`](fill.md) — act on the result.
