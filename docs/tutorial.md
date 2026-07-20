---
title: "Tutorial: Filling a Form End-to-End"
---

This tutorial walks through a realistic Vibium session: open a search engine,
type a query, submit the form, and capture the result. It exercises navigation,
mapping, semantic finding, form filling, waiting, and screenshots.

We'll use [https://duckduckgo.com](https://duckduckgo.com) as the target. Any@
search engine will work; just adjust the labels.

If you have Vibium installed globally, the examples run as written. If you'd
rather stay zero-install, run the same commands through `npx`:

```sh
npx -y vibium go https://duckduckgo.com
npx -y vibium find placeholder "Search privately"
# ...etc.
```

Or alias for the session:

```sh
alias vibium='npx -y vibium'
```

## 1. Open the page

```sh
vibium go https://duckduckgo.com
```

Vibium starts the browser if it isn't already running and navigates to the URL.

## 2. Find the search input

There are two equally good ways to locate the search box:

```sh
# By placeholder text
vibium find placeholder "Search privately"

# Or by ARIA role
vibium find role combobox
```

Either returns a reference like `@e1`.

You could also call `vibium map` to list every interactive element on the
page and pick a reference manually.

## 3. Fill the input and submit

```sh
vibium fill @e1 "vibium browser automation"
vibium press Enter
```

`press` sends a literal key event, which is the simplest way to submit a form
that reacts to Enter.

The `@eN` reference comes from the most recent `find` or `map` output. If the
page navigates or re-renders, run `find` or `map` again before reusing it.


> **Windows PowerShell**
>
> PowerShell treats `@` as special syntax. When using an element reference,
> wrap it in quotes:
>
> ```powershell
> vibium fill "@e1" "vibium browser automation"
> vibium click "@e1"
> ```

## 4. Wait for the results

The page transitions are asynchronous, so wait for something result-shaped to
appear before continuing. Any of these works:

```sh
vibium wait text "vibium"
vibium wait "h2"
```

## 5. Read and capture

```sh
vibium text > results.txt
vibium screenshot -o results.png
```

## 6. Record the whole session (optional)

If you want a replay of the whole interaction, wrap it in a recording. Run
the steps individually so each `find` result is visible before you act on
its reference:

```sh
vibium record start
vibium go https://duckduckgo.com
vibium find placeholder "Search privately"   # note the @eN it returns, e.g. @e1
vibium fill @e1 "vibium"
vibium press Enter
vibium wait text "vibium"
vibium record stop   # writes record.zip
```

`record.zip` contains the captured screenshots and is convenient for sharing
failures, debugging tests, attaching to a bug report, or playing back in the
[Vibium Record Player](https://player.vibium.dev/).

## What you just learned

- Drive a real browser with one command per step.
- Locate elements semantically (`find`), not with CSS selectors.
- Reference elements by stable `@eN` IDs.
- Fill, press, wait, and capture without juggling drivers.

Next up: read the [Core Concepts](concepts.md) page to understand how
mapping and references work under the hood, then dive into the
[Command Reference](/docs/commands/) for every flag.
