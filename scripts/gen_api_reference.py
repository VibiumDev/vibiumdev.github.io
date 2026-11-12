#!/usr/bin/env python3
"""Generate the client-library API references from the vibium API spec.

The spec is docs/reference/api.md in VibiumDev/vibium: one table row per
operation, with its wire, CLI, MCP, JS, Python, and Java form. CI in that
repo checks every column against the built binary and clients, so the
spec is the one trustworthy cross-surface listing.

This script reads the spec at two refs (the latest nightly tag and the
latest npm release tag) and emits:

  docs/libraries/{javascript,python,java}/api.md   per-language reference,
                                                   with typed signatures read
                                                   from the nightly's packages
  docs/reference/api-matrix.md                     every surface side by side
  site/public/api.json                             the same data for agents

Rows or cells present only at the nightly ref are marked "(nightly)".

Usage:
    python3 scripts/gen_api_reference.py
    python3 scripts/gen_api_reference.py --spec PATH --stable-spec PATH
"""
from __future__ import annotations

import argparse
import json
import re
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import api_details
from gen_command_reference import REPO_ROOT, WORK_DIR, gh_json, run

SPEC_PATH = "docs/reference/api.md"
RAW_URL = "https://raw.githubusercontent.com/VibiumDev/vibium/{ref}/" + SPEC_PATH
SOURCE_URL = "https://github.com/VibiumDev/vibium/blob/main/" + SPEC_PATH

LIBRARIES_DIR = REPO_ROOT / "docs" / "libraries"
MATRIX_PAGE = REPO_ROOT / "docs" / "reference" / "api-matrix.md"
API_JSON = REPO_ROOT / "site" / "public" / "api.json"
EXAMPLES_JSON = REPO_ROOT / "scripts" / "api-examples.json"

SURFACES = ("cli", "mcp", "javascript", "python", "java")
COLUMNS = ("id", "description", "wire", *SURFACES)
HEADER = ["#", "Description", "Wire Command", "CLI", "MCP", "JS", "Python", "Java"]
LANGUAGES = {
    "javascript": "JavaScript",
    "python": "Python",
    "java": "Java",
}
NOT_APPLICABLE = "—"
PLANNED = "⬜"
NIGHTLY = " **(nightly)**"
CHANGED = " **(changed in nightly)**"


@dataclass
class Row:
    section: str
    id: int
    description: str
    wire: str
    cells: dict[str, str] = field(default_factory=dict)

    def has(self, surface: str) -> bool:
        return self.cells[surface] not in (NOT_APPLICABLE, PLANNED)


def split_cells(line: str) -> list[str]:
    """Split a table row on pipes that are not inside a code span."""
    cells, current, in_code = [], [], False
    for ch in line.strip():
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
        else:
            current.append(ch)
    cells.append("".join(current).strip())
    return cells[1:-1]


def parse_spec(text: str) -> list[Row]:
    rows: list[Row] = []
    section = ""
    in_table = False
    for line in text.splitlines():
        if line.startswith("## "):
            section, in_table = line[3:].strip(), False
            continue
        if not line.startswith("|"):
            in_table = False
            continue
        cells = split_cells(line)
        if cells == HEADER:
            in_table = True
            continue
        if not in_table or set(line) <= set("|- "):
            continue
        if len(cells) != len(HEADER) or not cells[0].isdigit():
            raise SystemExit(f"gen_api_reference: cannot parse spec row: {line}")
        values = dict(zip(COLUMNS, cells))
        rows.append(
            Row(
                section=section,
                id=int(values["id"]),
                description=values["description"],
                wire=values["wire"],
                cells={s: values[s] for s in SURFACES},
            )
        )
    if not rows:
        raise SystemExit("gen_api_reference: no rows found in the spec")
    return rows


def fetch_spec(ref: str) -> str:
    with urllib.request.urlopen(RAW_URL.format(ref=ref)) as resp:
        return resp.read().decode("utf-8")


def latest_nightly_tag() -> str:
    releases = gh_json(
        "https://api.github.com/repos/VibiumDev/vibium/releases?per_page=15"
    )
    for release in releases:
        if release.get("prerelease") and release["tag_name"].startswith("nightly-"):
            return release["tag_name"]
    raise RuntimeError("no nightly release found")


def marker(row: Row, surface: str, stable: dict[int, Row]) -> str:
    """Nightly marker for one cell, compared with the stable spec."""
    old = stable.get(row.id)
    if old is None or not old.has(surface):
        return NIGHTLY
    if old.cells[surface] != row.cells[surface]:
        return CHANGED
    return ""


def table(header: list[str], body: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines.extend(
        "| " + " | ".join(c.replace("|", "\\|") for c in r) + " |" for r in body
    )
    return lines


def cell(value: str) -> str:
    return "" if value in (NOT_APPLICABLE, PLANNED) else value


def sections(rows: list[Row]) -> list[str]:
    seen: list[str] = []
    for row in rows:
        if row.section not in seen:
            seen.append(row.section)
    return seen


def same_text(a: str, b: str) -> bool:
    key = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    return key(a) == key(b) or key(a) in key(b)


def tidy(code: str) -> str:
    """Drop the `$1` suffixes the .d.ts bundler adds to duplicate names."""
    return re.sub(r"\$\d+\b", "", code)


def signature_lines(signatures: list[str]) -> list[str]:
    """One-line signatures as inline code; one that spans lines gets a fenced
    block. The block is plain text: token-level highlighting of a 25-parameter
    signature costs more HTML than the rest of its entry."""
    if any("\n" in s for s in signatures):
        return ["```text", "\n".join(signatures), "```", ""]
    if len(signatures) == 1:
        return [f"`{signatures[0]}`", ""]
    return [*(f"- `{s}`" for s in signatures), ""]


def load_examples(rows: list[Row]) -> dict[int, dict[str, str]]:
    """Hand-written examples keyed by spec row. scripts/verify_api_examples.py
    runs them; here they only have to point at rows that still exist."""
    examples = {int(k): v for k, v in json.loads(EXAMPLES_JSON.read_text()).items()}
    by_id = {r.id: r for r in rows}
    for row_id, by_lang in examples.items():
        row = by_id.get(row_id)
        if row is None:
            raise SystemExit(f"gen_api_reference: {EXAMPLES_JSON.name} has an example for row {row_id}, which the spec no longer has")
        for lang in by_lang:
            if not row.has(lang):
                raise SystemExit(f"gen_api_reference: row {row_id} has a {lang} example but no {lang} form in the spec")
    return examples


def emit_language_page(
    lang: str,
    rows: list[Row],
    stable: dict[int, Row],
    stable_version: str,
    details: api_details.Details | None,
    examples: dict[int, dict[str, str]],
) -> str:
    name = LANGUAGES[lang]
    count = sum(1 for r in rows if r.has(lang))
    parts = [
        "---",
        f"title: {name} API Reference",
        f"description: Every method in the Vibium {name} client with its typed signature, and the matching CLI command and MCP tool.",
        "tableOfContents:",
        "  maxHeadingLevel: 2",
        "---",
        "",
        f"<!-- Generated by scripts/gen_api_reference.py from {SPEC_PATH} and the nightly packages in VibiumDev/vibium. Do not edit. -->",
        "",
        f"All {count} entries of the {name} client API, grouped by object. Each",
        "entry shows the signature from the client's own source, then the",
        "matching CLI command and MCP tool where one exists.",
        "",
        f"Entries marked **(nightly)** are not in the latest release ({stable_version});",
        "**(changed in nightly)** means the documented signature differs from that release.",
        "Signatures come from the latest nightly build. See",
        "[What's in Nightly](../../nightly.md). The same data for every surface",
        "is in the [API matrix](../../reference/api-matrix.md) and in",
        "[`/api.json`](/api.json).",
        "",
    ]
    parts += [
        "Examples assume `bro` is a started browser and `vibe` is its page, as in the",
        "[quickstart](index.md).",
        "",
    ]
    if lang == "python":
        parts += [
            "Signatures are for the sync API (`from vibium import browser`). The async",
            "API in `vibium.async_api` has the same methods as coroutines.",
            "",
        ]
    shown: list[str] = []
    for section in sections(rows):
        entries = [r for r in rows if r.section == section and r.has(lang)]
        if not entries:
            continue
        parts += [f"## {section}", ""]
        for r in entries:
            member = details.lookup(r.cells[lang]) if details else None
            # A bold title, not a heading: Starlight wraps every heading in an
            # anchor icon, which on ~190 entries outweighs the page's text.
            parts += [f"**{r.cells[lang]}**", "", r.description + marker(r, lang, stable), ""]
            if member:
                signatures = [tidy(s) for s in member.signatures]
                shown += signatures
                parts += signature_lines(signatures)
                doc = re.split(r"\s@(?:param|returns?|throws|example)\b", member.doc)[0].strip()
                if doc and not same_text(doc, r.description):
                    parts += [doc, ""]
            example = examples.get(r.id, {}).get(lang)
            if example:
                parts += [f"Example: `{example}`", ""]
            equivalents = [
                f"{label} {r.cells[s]}"
                for s, label in (("cli", "CLI"), ("mcp", "MCP"))
                if r.has(s)
            ]
            if equivalents:
                parts += [" · ".join(equivalents), ""]
    if details:
        names = details.referenced_types(shown)
        blocks: dict[str, str] = {}
        for type_name in names:
            blocks.setdefault(tidy(type_name), tidy(details.types[type_name]))
        if blocks:
            parts += [
                "## Types",
                "",
                "Option and result types named in the signatures above.",
                "",
            ]
            for type_name in sorted(blocks):
                parts += [f"### `{type_name}`", "", f"```{details.fence}", blocks[type_name], "```", ""]
    return "\n".join(parts).rstrip() + "\n"


def emit_matrix_page(
    rows: list[Row], stable: dict[int, Row], stable_version: str
) -> str:
    parts = [
        "---",
        "title: API Matrix",
        "description: Every Vibium operation and its form on each surface, CLI, MCP, JavaScript, Python, and Java.",
        "tableOfContents:",
        "  maxHeadingLevel: 2",
        "---",
        "",
        f"<!-- Generated by scripts/gen_api_reference.py from {SPEC_PATH} in VibiumDev/vibium. Do not edit. -->",
        "",
        f"Every operation Vibium supports ({len(rows)} in all) and its form on each",
        "surface. An empty cell means the surface has no equivalent. The source",
        f"is the [API spec]({SOURCE_URL}) in the main repository, which CI checks",
        "against the binary and all three clients.",
        "",
        f"Operations marked **(nightly)** are not in the latest release ({stable_version}).",
        "The same data is published as [`/api.json`](/api.json). Per-language",
        "views: [JavaScript](../libraries/javascript/api.md),",
        "[Python](../libraries/python/api.md), [Java](../libraries/java/api.md).",
        "",
    ]
    for section in sections(rows):
        body = [
            [
                r.description + (NIGHTLY if r.id not in stable else ""),
                *(cell(r.cells[s]) for s in SURFACES),
            ]
            for r in rows
            if r.section == section and any(r.has(s) for s in SURFACES)
        ]
        if not body:
            continue
        parts += [f"## {section}", ""]
        parts += table(
            ["Operation", "CLI", "MCP", "JavaScript", "Python", "Java"], body
        )
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def plain(value: str) -> str | None:
    """A cell as data: no code ticks, None when the surface has no form."""
    return None if value in (NOT_APPLICABLE, PLANNED) else value.replace("`", "")


def emit_json(
    rows: list[Row],
    stable: dict[int, Row],
    stable_version: str,
    ref: str,
    details: dict[str, api_details.Details],
    examples: dict[int, dict[str, str]],
) -> str:
    operations = []
    for r in rows:
        if not any(r.has(s) for s in SURFACES):
            continue
        op = {
            "id": r.id,
            "section": r.section,
            "description": r.description,
            "wire": plain(r.wire),
            **{s: plain(r.cells[s]) for s in SURFACES},
            "nightlyOnly": [
                s for s in SURFACES if r.has(s) and marker(r, s, stable) == NIGHTLY
            ],
            "changedInNightly": [
                s for s in SURFACES if r.has(s) and marker(r, s, stable) == CHANGED
            ],
        }
        signatures = {
            lang: [tidy(s) for s in member.signatures]
            for lang in LANGUAGES
            if r.has(lang)
            and lang in details
            and (member := details[lang].lookup(r.cells[lang]))
        }
        if signatures:
            op["signatures"] = signatures
        if r.id in examples:
            op["examples"] = examples[r.id]
        operations.append(op)
    data = {
        "source": f"https://github.com/VibiumDev/vibium/blob/{ref}/{SPEC_PATH}",
        "stableVersion": stable_version,
        "surfaces": list(SURFACES),
        "operations": operations,
    }
    return json.dumps(data, indent=2, ensure_ascii=False) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", type=Path, help="api.md at the nightly ref")
    parser.add_argument("--stable-spec", type=Path, help="api.md at the release tag")
    parser.add_argument("--workdir", type=Path, default=WORK_DIR)
    args = parser.parse_args()

    stable_version = run(["npm", "view", "vibium", "dist-tags.latest"]).strip()
    tag = latest_nightly_tag()
    ref = "main" if args.spec else tag
    spec = args.spec.read_text() if args.spec else fetch_spec(ref)
    stable_spec = (
        args.stable_spec.read_text()
        if args.stable_spec
        else fetch_spec(f"v{stable_version}")
    )
    print(f"api spec: {ref} vs v{stable_version}")

    rows = parse_spec(spec)
    stable = {r.id: r for r in parse_spec(stable_spec)}
    details = api_details.load(tag, args.workdir)
    examples = load_examples(rows)
    for lang, found in details.items():
        cells = [r.cells[lang] for r in rows if r.has(lang)]
        print(f"  {lang}: signatures for {sum(1 for c in cells if found.lookup(c))} of {len(cells)}")

    for lang in LANGUAGES:
        page = LIBRARIES_DIR / lang / "api.md"
        page.parent.mkdir(parents=True, exist_ok=True)
        page.write_text(
            emit_language_page(
                lang, rows, stable, stable_version, details.get(lang), examples
            )
        )
    MATRIX_PAGE.parent.mkdir(parents=True, exist_ok=True)
    MATRIX_PAGE.write_text(emit_matrix_page(rows, stable, stable_version))
    API_JSON.write_text(emit_json(rows, stable, stable_version, ref, details, examples))
    print(
        f"wrote {len(LANGUAGES)} language references, api-matrix.md, and api.json "
        f"({len(rows)} operations)"
    )


if __name__ == "__main__":
    main()
