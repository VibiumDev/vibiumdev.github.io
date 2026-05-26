#!/usr/bin/env python3
"""Sync docs/ -> site/src/content/docs/docs/ for Starlight.

The source Markdown/MDX in `docs/` is already Starlight-shaped (title in
frontmatter, no leading H1), so this script does two small things:

  1. Copy each `.md`/`.mdx` file under a `docs/` slug prefix.
  2. Rewrite intra-doc `.md` links to Starlight root URLs
     (`[…](foo.md)` -> `[…](/docs/foo/)`).
"""
from __future__ import annotations

import re
import shutil
import posixpath
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "docs"
DEST = REPO_ROOT / "site" / "src" / "content" / "docs"
ROUTE_PREFIX = "docs"

MD_LINK_RE = re.compile(r"(\]\()([^)\s]+?)\.md(#[^)]+)?(\))")
CONTENT_SUFFIXES = {".md", ".mdx"}


def rewrite_md_links(text: str, rel: Path) -> str:
    def repl(m: re.Match) -> str:
        prefix, target = m.group(1), m.group(2)
        anchor, suffix = m.group(3) or "", m.group(4)
        if target.startswith(("http://", "https://", "/")):
            return m.group(0)
        resolved = posixpath.normpath(posixpath.join(rel.parent.as_posix(), target))
        if resolved == "." or resolved.startswith("../"):
            return m.group(0)
        return f"{prefix}/{ROUTE_PREFIX}/{resolved}/{anchor}{suffix}"

    return MD_LINK_RE.sub(repl, text)


def main() -> None:
    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)

    count = 0
    for src in sorted(SRC.rglob("*")):
        if src.suffix not in CONTENT_SUFFIXES:
            continue
        rel = src.relative_to(SRC)
        target = DEST / ROUTE_PREFIX / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        text = rewrite_md_links(src.read_text(encoding="utf-8"), rel)
        target.write_text(text, encoding="utf-8")
        count += 1

    print(f"synced {count} files -> {DEST.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
