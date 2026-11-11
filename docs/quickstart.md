---
title: Quickstart
---

The shortest possible end-to-end session: open a page, capture it, and
read something back. Pick
your surface in the header, or read all five.

```sh title="CLI"
npm install -g vibium
vibium go https://example.com
vibium screenshot -o example.png
vibium text
```

```sh title="MCP"
claude mcp add vibium -- npx -y vibium mcp
# Then ask the agent:
#   Use Vibium to open https://example.com, take a screenshot,
#   and tell me what the page says.
```

```javascript
// npm install vibium
import { writeFileSync } from 'node:fs'
import { browser } from 'vibium'

const bro = await browser.start()
const vibe = await bro.page()

await vibe.go('https://example.com')
writeFileSync('example.png', await vibe.screenshot())
console.log(await vibe.title())

await bro.stop()
```

```python
# pip install vibium
from vibium import browser

bro = browser.start()
vibe = bro.page()

vibe.go("https://example.com")
with open("example.png", "wb") as f:
    f.write(vibe.screenshot())
print(vibe.title())

bro.stop()
```

```java
// implementation 'com.vibium:vibium:26.8.21'
import com.vibium.Vibium;
import java.nio.file.Files;
import java.nio.file.Path;

public class Quickstart {
    public static void main(String[] args) throws Exception {
        var bro = Vibium.start();
        var vibe = bro.page();

        vibe.go("https://example.com");
        Files.write(Path.of("example.png"), vibe.screenshot());
        System.out.println(vibe.title());

        bro.stop();
    }
}
```

In the libraries, `screenshot()` returns the PNG as bytes and you write the
file yourself. Longer walkthroughs: [CLI](cli/index.md),
[MCP](mcp/setup.md), [JavaScript](libraries/javascript/index.md),
[Python](libraries/python/index.md), [Java](libraries/java/index.md).

## CLI in detail

The CLI commands above open a page, save a screenshot, and print the page
text.

> **Why does `vibium text` not need a URL or selector?** Vibium keeps a
> background browser running across commands; later commands act on the
> page opened by the most recent `vibium go`. See
> [Core Concepts](concepts.md) for the full mental model.

What you should see:

- `vibium go https://example.com` — exits with status 0; the browser
  navigates to the page. No output on stdout is normal.
- `vibium screenshot -o example.png` — writes the PNG to
  `~/Pictures/Vibium/example.png` and prints the saved path to stdout. The
  CLI manages screenshot storage for you; `-o` controls the *filename*, not
  the directory. `ls -lh ~/Pictures/Vibium/example.png` should show a
  non-empty PNG.
- `vibium text` — prints the visible page text to stdout. For
  `https://example.com` that is a short notice that the domain is for
  documentation examples.

If any of those don't match, see [Troubleshooting](troubleshooting.md).

## Zero-install with `npx`

If you'd rather not install anything, the same flow works through `npx`:

```sh
npx -y vibium go https://example.com
npx -y vibium screenshot -o example.png
npx -y vibium text
```

This is great for CI jobs, throwaway scripts, and demos. To make the rest of
this guide copy-pasteable, alias it for the current shell:

```sh
alias vibium='npx -y vibium'
vibium go https://example.com
vibium text
```

## Let the AI drive

> Nightly builds and the next npm release; see [Run and Check](run-and-check.md).

With an AI provider configured (`vibium setup` asks the questions and writes
the config), a whole goal is one command:

```sh
vibium run "open example.com and find its contact page"
vibium check "the page shows contact information"
```

`run` drives the browser toward the goal and reports COMPLETED or
NOT_COMPLETED; `check` independently verifies a claim with PASS, FAIL, or
REVIEW. See [Run and Check](run-and-check.md).

## Agent skill

```sh
npm install -g vibium
vibium add-skill
```

This installs the `browser` and `check` skills for each supported agent
already on the machine (Claude Code, Grok). After this, your agent can drive
the browser by emitting `vibium ...` commands.

See the [Tutorial](tutorial.md) for a longer worked example.
