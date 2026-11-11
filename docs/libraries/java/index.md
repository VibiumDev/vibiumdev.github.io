---
title: Java
description: Add the Vibium Java client with Gradle or Maven and run a first program.
---

`com.vibium:vibium` on Maven Central drives a real browser from Java. The
artifact bundles the `vibium` binary for every supported platform.

## Requirements

- Java 11 or newer
- Linux x64/arm64, macOS x64/arm64, or Windows x64

## Install

Gradle:

```groovy
dependencies {
    implementation 'com.vibium:vibium:26.8.21'
}
```

Maven:

```xml
<dependency>
    <groupId>com.vibium</groupId>
    <artifactId>vibium</artifactId>
    <version>26.8.21</version>
</dependency>
```

Chrome for Testing downloads the first time a browser starts.

## First program

Save this as `src/main/java/Hello.java`:

```java
import com.vibium.Vibium;
import com.vibium.types.SelectorOptions;
import java.nio.file.Files;
import java.nio.file.Path;

public class Hello {
    public static void main(String[] args) throws Exception {
        // Launch a browser. The window is visible by default.
        var bro = Vibium.start();
        var vibe = bro.page();

        vibe.go("https://example.com");
        Files.write(Path.of("screenshot.png"), vibe.screenshot());

        var link = vibe.find(new SelectorOptions().role("link"));
        System.out.println("Found link: " + link.text());
        link.click();

        bro.stop();
    }
}
```

Run it with Gradle (`application { mainClass = 'Hello' }` in
`build.gradle`):

```sh
gradle run
```

Or with Maven:

```sh
mvn compile exec:java -Dexec.mainClass=Hello
```

A Chrome window opens, loads the page, clicks the link, and closes. The
program prints `Found link: Learn more` and leaves `screenshot.png` in the
folder.

| Call | What it does |
| --- | --- |
| `Vibium.start()` | Launches Chrome and returns a Browser |
| `bro.page()` | Returns the default page (tab) |
| `vibe.go(url)` | Navigates to a URL |
| `vibe.screenshot()` | Returns the page as PNG bytes |
| `vibe.find(new SelectorOptions().role("link"))` | Finds an element by its accessible role |
| `link.click()` | Clicks the element |
| `bro.stop()` | Closes the browser |

## Options

Options are builder objects in `com.vibium.types`. Hide the browser window:

```java
import com.vibium.types.StartOptions;

var bro = Vibium.start(new StartOptions().headless(true));
```

Launch Firefox instead of Chrome:

```java
var bro = Vibium.start(new StartOptions().engine("firefox"));
```

See [Using Firefox](../../using-firefox.md) for engine details.

## Finding elements

`SelectorOptions` holds semantic locators. They survive markup changes
better than CSS:

```java
vibe.find(new SelectorOptions().role("button").text("Sign in"));
vibe.find(new SelectorOptions().label("Email"));
vibe.find(new SelectorOptions().placeholder("Search..."));
vibe.find(new SelectorOptions().testid("checkout"));
```

> **Nightly only.** A bare string is a plain-language description
> (`vibe.find("the Add to Cart button")`), and `.css("...")` takes an exact
> CSS selector. In 26.8.21 a bare string is a CSS selector. The builder
> forms above work in both.

## Let the AI drive

> **Nightly only.** See [Run and Check](../../run-and-check.md).

```java
var result = vibe.run("open the contact page");
var verdict = vibe.check("the page lists an email address");
```

## Custom binary

Set `VIBIUM_BIN_PATH` to use your own build of the binary:

```sh
export VIBIUM_BIN_PATH=/path/to/your/vibium
```

## Next

- [API Reference](api.md): every method, with its CLI and MCP equivalent.
- [Client Libraries](../index.md): the object model shared by all three languages.
- [Run and Check](../../run-and-check.md) and [Model Providers](../../ai-providers.md).
- [Troubleshooting](../../troubleshooting.md).
