#!/usr/bin/env python3
"""Generate public llms.txt assets for the Vibium documentation.

Usage:
    python3 scripts/build_llms_txt.py [--output PATH]

The generated `llms.txt` follows https://llmstxt.org/: a concise Markdown
index with an H1, summary blockquote, optional notes, and H2-delimited lists
of links to Markdown resources.

For agents that still want one large context file, the script also writes
`llms-full.txt`, which concatenates the ordered source docs.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Doc:
    """A Markdown document that should be exposed through llms.txt."""

    path: str
    section: str


# Ordered list of doc files, relative to the repo root. New docs should be
# added here in the order they should appear in llms.txt and llms-full.txt.
DOCS: list[Doc] = [
    Doc("README.md", "Optional"),
    Doc("docs/introduction.md", "Docs"),
    Doc("docs/installation.md", "Docs"),
    # Reading order intentionally puts Quickstart before Getting Started:
    # Quickstart is the copy-paste onramp, Getting Started is the deeper
    # mental-model walk-through.
    Doc("docs/quickstart.md", "Docs"),
    Doc("docs/getting-started.md", "Docs"),
    Doc("docs/tutorial.md", "Docs"),
    Doc("docs/concepts.md", "Docs"),
    Doc("docs/mcp-integration.md", "Docs"),
    Doc("docs/client-libraries.md", "Docs"),
    Doc("docs/troubleshooting.md", "Docs"),
    Doc("docs/faq.md", "Docs"),
    Doc("docs/commands/index.md", "Command Reference"),
    Doc("docs/commands/go.md", "Command Reference"),
    Doc("docs/commands/map.md", "Command Reference"),
    Doc("docs/commands/diff.md", "Command Reference"),
    Doc("docs/commands/find.md", "Command Reference"),
    Doc("docs/commands/click.md", "Command Reference"),
    Doc("docs/commands/fill.md", "Command Reference"),
    Doc("docs/commands/select.md", "Command Reference"),
    Doc("docs/commands/check.md", "Command Reference"),
    Doc("docs/commands/press.md", "Command Reference"),
    Doc("docs/commands/wait.md", "Command Reference"),
    Doc("docs/commands/text.md", "Command Reference"),
    Doc("docs/commands/screenshot.md", "Command Reference"),
    Doc("docs/commands/pdf.md", "Command Reference"),
    Doc("docs/commands/eval.md", "Command Reference"),
    Doc("docs/commands/record.md", "Command Reference"),
    Doc("docs/commands/mcp.md", "Command Reference"),
    Doc("docs/contributing.md", "Optional"),
]

FRONTMATTER_RE = re.compile(r"\A---\n(?P<frontmatter>.*?)\n---\n", re.DOTALL)
TITLE_RE = re.compile(r"^title:\s*(?P<title>.+?)\s*$", re.MULTILINE)
LINK_ITEM_RE = re.compile(r"-\s+\[[^\]]+\]\([^)]+\)(?::\s+.+)?$")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
MARKDOWN_EMPHASIS_RE = re.compile(r"[*_]{1,3}([^*_]+)[*_]{1,3}")
FIRST_SENTENCE_RE = re.compile(r"^(.+?[.!?])(?:\s|$)")

PROJECT_TITLE = "Vibium"
PROJECT_SUMMARY = "Browser automation for AI agents and humans, built on WebDriver BiDi."


def normalize_base_path(value: str) -> str:
    trimmed = value.strip()
    if not trimmed or trimmed == "/":
        return ""
    return "/" + trimmed.strip("/")


def site_origin() -> str:
    site = os.environ.get("SITE_URL", "https://vibium.com").strip().rstrip("/")
    base = normalize_base_path(os.environ.get("BASE_PATH", "/"))
    return f"{site}{base}"


def strip_frontmatter(text: str) -> tuple[str | None, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, text

    frontmatter = match.group("frontmatter")
    title_match = TITLE_RE.search(frontmatter)
    title = title_match.group("title").strip("\"'") if title_match else None
    return title, text[match.end() :]


def metadata(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    title, body = strip_frontmatter(text)
    lines = body.splitlines()

    if title is None:
        for i, line in enumerate(lines):
            if line.startswith("# "):
                title = line[2:].strip()
                lines = lines[i + 1 :]
                break

    if title is None:
        title = path.stem.replace("-", " ").title()

    paragraphs: list[str] = []
    current: list[str] = []
    in_fence = False
    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not line:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        if line.startswith(("#", "-", ">", "|")):
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append(" ".join(current))

    desc = summarize(paragraphs[0] if paragraphs else "Vibium documentation.")
    return title, desc


def summarize(text: str, max_len: int = 180) -> str:
    text = MARKDOWN_LINK_RE.sub(r"\1", text)
    text = MARKDOWN_EMPHASIS_RE.sub(r"\1", text)
    text = " ".join(text.split())

    sentence = FIRST_SENTENCE_RE.match(text)
    if sentence:
        text = sentence.group(1)

    if len(text) <= max_len:
        return text

    shortened = text[: max_len - 3].rsplit(" ", 1)[0]
    return shortened.rstrip(".,;:") + "..."


def markdown_url(origin: str, rel: str) -> str:
    return f"{origin}/llms/{rel}"


def build_llms_txt(repo_root: Path, docs: list[Doc]) -> str:
    origin = site_origin()
    lines = [
        f"# {PROJECT_TITLE}",
        "",
        f"> {PROJECT_SUMMARY}",
        "",
        "This file is a curated index of the Vibium documentation for LLMs. "
        "The linked files are clean Markdown copies generated from the "
        "canonical repository docs.",
        "",
        "Use `llms-full.txt` when a single expanded context file is more useful "
        "than following individual links.",
        "",
    ]

    sections: dict[str, list[str]] = {}
    missing: list[str] = []
    for doc in docs:
        path = repo_root / doc.path
        if not path.is_file():
            missing.append(doc.path)
            continue
        title, desc = metadata(path)
        sections.setdefault(doc.section, []).append(
            f"- [{title}]({markdown_url(origin, doc.path)}): {desc}"
        )

    if missing:
        raise SystemExit(
            "build_llms_txt: missing files referenced in DOCS:\n  - "
            + "\n  - ".join(missing)
        )

    for section in ("Docs", "Command Reference", "Optional"):
        items = sections.get(section)
        if not items:
            continue
        lines.append(f"## {section}")
        lines.append("")
        lines.extend(items)
        lines.append("")

    text = "\n".join(lines).rstrip() + "\n"
    validate_llms_txt(text)
    return text


def build_llms_full(repo_root: Path, docs: list[Doc]) -> str:
    parts: list[str] = []
    generated_at = _dt.datetime.now(_dt.timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )
    parts.append(
        "\n".join(
            [
                "# Vibium Documentation Context",
                "",
                PROJECT_SUMMARY,
                "",
                "This file is a single-document concatenation of the Vibium "
                "documentation for agent consumption. It is generated from the "
                "Markdown sources by `scripts/build_llms_txt.py`. Edit the "
                "sources, not this file.",
                "",
                "The spec-compliant llms.txt index is available at `/llms.txt`.",
                "",
                f"Generated: {generated_at}",
                "",
            ]
        )
    )

    missing: list[str] = []
    for doc in docs:
        path = repo_root / doc.path
        if not path.is_file():
            missing.append(doc.path)
            continue
        body = path.read_text(encoding="utf-8").rstrip() + "\n"
        parts.append(f"\n\n--- file: {doc.path} ---\n\n")
        parts.append(body)

    if missing:
        raise SystemExit(
            "build_llms_txt: missing files referenced in DOCS:\n  - "
            + "\n  - ".join(missing)
        )

    return "".join(parts)


def validate_llms_txt(text: str) -> None:
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# ") or lines[0].startswith("## "):
        raise SystemExit("build_llms_txt: llms.txt must start with a single H1")

    in_file_list = False
    h2_count = 0
    for lineno, line in enumerate(lines[1:], start=2):
        if line.startswith("# "):
            raise SystemExit(f"build_llms_txt: unexpected H1 on line {lineno}")
        if line.startswith("###"):
            raise SystemExit(
                f"build_llms_txt: only H1 and H2 headings are allowed; line {lineno}"
            )
        if line.startswith("## "):
            in_file_list = True
            h2_count += 1
            continue
        if not line.strip():
            continue
        if in_file_list and not LINK_ITEM_RE.fullmatch(line):
            raise SystemExit(
                "build_llms_txt: H2 sections must contain only markdown link "
                f"list items; line {lineno}: {line}"
            )

    if h2_count == 0:
        raise SystemExit("build_llms_txt: expected at least one H2 file-list section")


def mirror_markdown(repo_root: Path, docs: list[Doc], public_dir: Path) -> int:
    mirror_dir = public_dir / "llms"
    if mirror_dir.exists():
        shutil.rmtree(mirror_dir)

    count = 0
    for doc in docs:
        src = repo_root / doc.path
        target = mirror_dir / doc.path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, target)
        count += 1

    return count


def write_outputs(repo_root: Path, output: Path, llms_text: str, full_text: str) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(llms_text, encoding="utf-8")

    full_output = output.with_name("llms-full.txt")
    full_output.write_text(full_text, encoding="utf-8")
    mirror_count = mirror_markdown(repo_root, DOCS, output.parent)

    size_kb = len(llms_text.encode("utf-8")) / 1024
    full_size_kb = len(full_text.encode("utf-8")) / 1024
    display_output = (
        output.relative_to(repo_root) if output.is_relative_to(repo_root) else output
    )
    display_full_output = (
        full_output.relative_to(repo_root)
        if full_output.is_relative_to(repo_root)
        else full_output
    )
    print(
        f"wrote {display_output} ({len(DOCS)} links, {size_kb:.1f} KB) "
        f"and {display_full_output} ({full_size_kb:.1f} KB)"
    )
    mirror_dir = output.parent / "llms"
    display_mirror_dir = (
        mirror_dir.relative_to(repo_root)
        if mirror_dir.is_relative_to(repo_root)
        else mirror_dir
    )
    print(f"mirrored {mirror_count} markdown files -> {display_mirror_dir}/")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output path (default: <repo_root>/site/public/llms.txt).",
    )
    args = parser.parse_args()

    # Repo root is the parent of the `scripts/` directory containing this file.
    repo_root = Path(__file__).resolve().parent.parent
    output = (
        Path(args.output).resolve()
        if args.output
        else repo_root / "site" / "public" / "llms.txt"
    )

    llms_text = build_llms_txt(repo_root, DOCS)
    full_text = build_llms_full(repo_root, DOCS)
    write_outputs(repo_root, output, llms_text, full_text)


if __name__ == "__main__":
    main()
