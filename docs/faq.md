---
title: FAQ
---

## How is Vibium different from Selenium / Playwright / Puppeteer?

Vibium targets **AI agents first** and humans second. Its surface area is
small and verb-shaped (`go`, `map`, `click`, `fill`), its element references
are short and human-readable (`@e1`), and it favors semantic locators
(text, label, placeholder, role) over CSS selectors. The result is a tool an
LLM can use correctly with very little prompting.

Under the hood it speaks W3C [WebDriver BiDi](https://w3c.github.io/webdriver-bidi/),
the same standards-track protocol the wider browser-automation ecosystem is
moving toward.

## Which browsers does it support?

Chrome and Firefox. Vibium ships with its own managed Google Chrome for
Testing build, downloaded automatically on first use; Firefox is one
`vibium install --engine firefox` (or just `--engine firefox` on any
command) away. Both are driven over WebDriver BiDi. See
[Using Firefox](using-firefox.md).

## Can Vibium drive the browser with AI?

Yes — in the nightly builds and the next npm release. `vibium run "<goal>"`
hands a goal to a configured model, which drives the browser tools itself;
`vibium check "<claim>"` independently verifies an outcome. Providers:
OpenAI, Anthropic, Google, xAI, or any OpenAI-compatible (including local)
server. See [Run and Check](run-and-check.md).

## Do I need to install a separate driver?

No. Vibium is one ~10 MB binary. It downloads Chrome for Testing together
with the matching `chromedriver` and manages both; `vibium paths` shows where
they live. Firefox needs no driver at all. There is no profile directory you
have to maintain.

## Do I need to install Vibium at all?

No. Every command works through `npx`:

```sh
npx -y vibium go https://example.com
npx -y vibium screenshot -o page.png
npx -y vibium text
```

This is convenient for CI jobs, throwaway scripts, sandboxes, or any host
where you'd rather not install software globally. See
[Installation](installation.md) for details.

## Can I run Vibium headlessly on CI?

Yes. Pass `--headless` (every command and `vibium mcp` accept it) so the
browser runs without a window; a host with no display needs it, or a virtual
display such as `xvfb-run`. Capture commands (`screenshot`, `text`, `pdf`)
work the same way as on a desktop. Pin the browser with
`VIBIUM_ENGINE_VERSION` to keep a CI fleet on one version.

## Can two scripts drive browsers at the same time?

Yes — give each its own named session with `--session <name>` or
`VIBIUM_SESSION`. Each session gets its own daemon and browser. See
[Concurrent sessions](sessions.md).

## Is there a Python / TypeScript / Java SDK?

Yes — see [Client Libraries](libraries/index.md). All three wrap the same
binary, so behavior is identical across languages.

## How do I plug it into Codex or another agent?

Register Vibium as an MCP server. See [MCP Server Integration](mcp/index.md).

## Why semantic locators instead of CSS selectors?

CSS selectors are brittle: a refactor of class names breaks all your tests.
They are also hard for an LLM to produce reliably. Semantic locators
(`find text "Sign in"`, `find label "Email"`, `find role button`) describe
what a human would describe, which is also what an LLM tends to produce
naturally.

`vibium eval` is still available when you genuinely need a CSS or XPath
selector for something the semantic API can't express.

## What's the license?

Apache 2.0.

## Where does Vibium store data?

The bundled browser and any cached state live in Vibium's data directory.
Removing that directory wipes Vibium's local state without affecting your
system Chrome.
