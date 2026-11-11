# Vibium Website

[![Agent readability: 33/100](https://img.shields.io/badge/a14y-33%2F100-c2410c?label=agent%20readability)](https://a14y.dev/badge/?s=33&v=0.2.0&a=24&t=38&p=8&f=16&w=0&e=0&n=14&d=2026-05-26&m=site&u=https%3A%2F%2Fvibium.com%2F)

Browser automation for AI agents and humans, built on WebDriver BiDi.

This repository contains the user-facing [Vibium](https://github.com/VibiumDev/vibium)
website and documentation. The homepage is an Astro page at `/`, while the
documentation is published under `/docs/`.

The docs are plain Markdown so they render well on GitHub, in Starlight, and
inside an agent context window.

## Contents

- [Introduction](docs/introduction.md)
- [Installation](docs/installation.md)
- [Quickstart](docs/quickstart.md) — one session on every surface.
- [Tutorial: Filling a Form End-to-End](docs/tutorial.md) — a worked example.
- [Core Concepts](docs/concepts.md)
- [Troubleshooting](docs/troubleshooting.md)
- [FAQ](docs/faq.md)
- [Contributing](docs/contributing.md)

By surface:

- CLI: [Getting Started](docs/cli/index.md), [Command Reference](docs/commands/index.md)
- MCP: [MCP Server](docs/mcp/index.md), [Client Setup](docs/mcp/setup.md)
- Libraries: [Overview](docs/libraries/index.md),
  [JavaScript](docs/libraries/javascript/index.md),
  [Python](docs/libraries/python/index.md),
  [Java](docs/libraries/java/index.md)

## Site generation

The top-level `Makefile` is the build entrypoint:

- `make build` regenerates public LLM docs, syncs Markdown and MDX into
  Starlight, builds the static site in `site/dist/`, and postprocesses the
  generated output for agent-readable surfaces.
- `make rebuild` removes generated site output first, then runs the full build.
- `make serve` regenerates content and starts the local Astro dev server.
- `make test` builds the site and verifies the homepage, `/docs/` routes,
  root LLM assets, agent-readable generated files, and Google Analytics wiring.
- `make clean` removes generated output listed in `scripts/clean-manifest.txt`
  and deletes stray `.DS_Store` files.

Edit the homepage in `site/src/pages/index.astro`. Edit canonical docs content
in `README.md` and `docs/`; `scripts/sync_starlight.py` copies those files into
Starlight under `/docs/`.

Edit canonical brand imagery in `site/src/assets/brand/` and landing page
imagery in `site/src/assets/landing/`. The favicon files in `site/public/` are
stable served assets.

The generated `site/public/llms.txt` is a spec-compliant index served at
`/llms.txt`; it links to Markdown copies of the docs under `/llms/`. The
generated `site/public/llms-full.txt` keeps the single-file context form for
agents that prefer one large document, and `llms-<surface>.txt` (cli, mcp,
javascript, python, java) holds the shared docs plus one surface.

## Generated reference

`make reference` regenerates everything that comes from the product itself:

- `scripts/gen_command_reference.py`: `docs/commands/`, `docs/nightly.md`,
  and `/commands.json`, from the binaries' own help.
- `scripts/gen_api_reference.py`: `docs/libraries/*/api.md`,
  `docs/reference/api-matrix.md`, and `/api.json`, from
  `docs/reference/api.md` in the main repository.
- `scripts/gen_mcp_reference.py`: `docs/mcp/tools.md` and `/mcp-tools.json`,
  from the MCP server's `tools/list`.

- `scripts/import_upstream_docs.py`: the guides listed in
  `scripts/upstream-manifest.json`, imported from `docs/` in the main
  repository. To publish another upstream guide, add a line to the manifest.
  Its `aliases` map upstream pages to the site pages that replace them, so
  links between guides stay on the site.

Each compares the latest npm release with the latest nightly and marks what
only the nightly has. Do not edit the generated pages by hand; the daily
`refresh-reference` workflow overwrites them.

## Surfaces

The docs cover five surfaces: CLI, MCP, JavaScript, Python, and Java. Each
has its own sidebar topic (`site/astro.config.mjs`). Pages under `docs/cli/`,
`docs/mcp/`, and `docs/libraries/` register themselves in `llms.txt` and get
Markdown mirrors automatically; a new top-level page must be added to `DOCS`
in `scripts/build_llms_txt.py`, and `make test` fails if it is not.

Write examples as plain adjacent code fences, one per surface. A fence's
surface comes from `title="CLI|MCP|JavaScript|Python|Java"` or, without a
title, from its language. A shell fence counts as CLI only when every command
in it is a `vibium` command, so an install step is never filtered away. Two or more adjacent fences for different surfaces
become a group that the header picker filters
(`site/src/plugins/remark-surface-groups.mjs`). Nothing is hidden until a
reader picks a surface, and the Markdown mirrors always keep every block.

`scripts/postprocess_site.py` runs after Astro builds. It writes same-path
Markdown mirrors into `site/dist/`, adds language classes to generated code
blocks, adds `<lastmod>` values to the XML sitemap, and publishes
`site/dist/sitemap.md`.

## Agent readability

The badge above reflects the latest live `https://vibium.com/` a14y site audit.
To check unpublished changes locally, build with a localhost `SITE_URL`, preview
the static output, and run the site audit against that preview:

```sh
SITE_URL=http://127.0.0.1:4323 make build
pnpm --dir site exec astro preview --host 127.0.0.1 --port 4323
npx -y a14y check http://127.0.0.1:4323/ --mode site --output agent-prompt --max-pages 200
```

After deployment, refresh the badge with the `Embed badge:` URL printed by:

```sh
npx -y a14y check https://vibium.com/ --mode site --max-pages 200
```
