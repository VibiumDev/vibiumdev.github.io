---
title: Contributing
---

Thanks for considering a contribution to Vibium. The canonical contributing
guide lives at <https://github.com/VibiumDev/vibium/blob/main/CONTRIBUTING.md>;
this page summarizes the most important pieces.

## Develop in a VM

Because Vibium is exercised heavily by AI-assisted tools during development,
contributors are encouraged to work inside a VM to contain potential side
effects. Platform-specific setup guides for macOS, Linux x86, and Windows
x86 live under `docs/how-to-guides/` in the main repository.

## Toolchain prerequisites

To build the full project you'll want:

- Go 1.21+
- Node.js 18+
- Python 3.9+
- Java 21+ with Gradle 8+
- (Optional) GitHub CLI

The Go toolchain builds the core binary; Node, Python, and Java are needed
for their respective client libraries.

## Build and test

After cloning the repository:

```sh
make
make test
```

`make` installs dependencies, compiles the binary, downloads the managed
browser, and builds each client library. `make test` runs the test suites.
There are also more granular targets for building or testing individual
components — see the `Makefile` for the full list.

## Working on the clients

Each client library can be built and tested in isolation:

- **JavaScript** — under `clients/javascript`. Both sync and async APIs ship,
  and the sync API is convenient in a Node REPL.
- **Python** — run `uv sync` from the Python client directory. The client
  locates the bundled binary automatically, or honors `VIBIUM_BIN_PATH`.
- **Java** — published to Maven Central with native binaries bundled. Compile
  examples against the built JAR and dependency directory.

## Workflow

- **Team members** can push directly to the main repository.
- **External contributors** should fork, push to their fork, and open a pull
  request against `main`.

## Reporting bugs

When reporting an issue, please include:

- Your platform and architecture.
- The exact command(s) and full output.
- The Vibium version (`vibium --version`).
- A `record.zip` from a `vibium record` session if the bug is interactive.

## Documentation contributions

This `vibium-docs` site is a separate Markdown collection. To update a doc:

1. Edit the relevant Markdown file.
2. Run `make build` so generated LLM docs and the Starlight site stay in sync.
3. Open a pull request.

Canonical brand imagery lives in `site/src/assets/brand/`. Files in
`site/public/` are served build inputs; update stable favicons there when the
served icon set changes.
