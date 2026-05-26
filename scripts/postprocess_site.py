#!/usr/bin/env python3
"""Apply generated-site polish that Astro/Starlight do not emit directly."""

from __future__ import annotations

import datetime as _dt
import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from build_llms_txt import DOCS, metadata, strip_frontmatter


PRE_RE = re.compile(r"<pre(?P<attrs>[^>]*)data-language=\"(?P<lang>[^\"]+)\"(?P<after>[^>]*)>")
URL_RE = re.compile(r"<url>(?P<body>.*?)</url>")
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def yaml_scalar(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def today() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%d")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def mirror_markdown_page(src: Path, target: Path, last_updated: str) -> None:
    title, description = metadata(src)
    _, body = strip_frontmatter(src.read_text(encoding="utf-8"))
    frontmatter = "\n".join(
        [
            "---",
            f"title: {yaml_scalar(title)}",
            f"description: {yaml_scalar(description)}",
            'doc_version: "vibium-docs"',
            f"last_updated: {last_updated}",
            "---",
            "",
        ]
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    sitemap = "\n\n## Sitemap\n\n- [LLM docs index](/llms.txt)\n"
    target.write_text(frontmatter + body.lstrip().rstrip() + sitemap, encoding="utf-8")


def write_markdown_mirrors(root: Path, dist: Path, last_updated: str) -> int:
    count = 0
    mirror_markdown_page(root / "README.md", dist / "index.md", last_updated)
    count += 1
    mirror_markdown_page(root / "docs" / "index.mdx", dist / "docs.md", last_updated)
    mirror_markdown_page(root / "docs" / "index.mdx", dist / "docs" / "index.md", last_updated)
    count += 2

    for doc in DOCS:
        if doc.path == "README.md":
            continue
        src = root / doc.path
        if doc.path == "docs/commands/index.md":
            targets = [dist / "docs" / "commands.md", dist / doc.path]
        else:
            targets = [dist / doc.path]
        for target in targets:
            mirror_markdown_page(src, target, last_updated)
            count += 1

    return count


def language_class(lang: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9-]+", "-", lang.strip().lower()).strip("-")
    return f"language-{cleaned or 'text'}"


def add_pre_language_classes(html_text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        after = match.group("after")
        cls = language_class(match.group("lang"))
        combined_attrs = attrs + after
        class_match = re.search(r'class="([^"]*)"', combined_attrs)
        if class_match:
            classes = class_match.group(1).split()
            if cls not in classes:
                classes.append(cls)
            combined_attrs = (
                combined_attrs[: class_match.start(1)]
                + html.escape(" ".join(classes), quote=True)
                + combined_attrs[class_match.end(1) :]
            )
            return f"<pre{combined_attrs} data-language=\"{match.group('lang')}\">"
        return f"<pre class=\"{cls}\"{attrs} data-language=\"{match.group('lang')}\"{after}>"

    return PRE_RE.sub(replace, html_text)


def postprocess_html(dist: Path) -> int:
    count = 0
    for path in dist.rglob("*.html"):
        text = path.read_text(encoding="utf-8")
        updated = add_pre_language_classes(text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            count += 1
    return count


def add_sitemap_lastmod(dist: Path, last_updated: str) -> int:
    count = 0
    for path in dist.glob("sitemap-*.xml"):
        if path.name == "sitemap-index.xml":
            continue
        text = path.read_text(encoding="utf-8")

        def replace(match: re.Match[str]) -> str:
            body = match.group("body")
            if "<lastmod>" in body:
                return match.group(0)
            return f"<url>{body}<lastmod>{last_updated}</lastmod></url>"

        updated = URL_RE.sub(replace, text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            count += 1
    return count


def write_sitemap_markdown(dist: Path) -> int:
    pages: list[str] = []
    for path in sorted(dist.glob("sitemap-*.xml")):
        if path.name == "sitemap-index.xml":
            continue
        sitemap = ET.parse(path)
        for loc in sitemap.findall(".//sm:loc", SITEMAP_NS):
            if loc.text:
                pages.append(loc.text.strip())

    if not pages:
        return 0

    lines = ["# Sitemap", "", "HTML pages published by the Vibium documentation site.", ""]
    lines.extend(f"- [{page}]({page})" for page in pages)
    (dist / "sitemap.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return 1


def main() -> None:
    root = repo_root()
    dist = root / "site" / "dist"
    if not dist.is_dir():
        raise SystemExit("postprocess_site: site/dist does not exist; run Astro build first")

    last_updated = today()
    mirror_count = write_markdown_mirrors(root, dist, last_updated)
    html_count = postprocess_html(dist)
    sitemap_count = add_sitemap_lastmod(dist, last_updated)
    sitemap_md_count = write_sitemap_markdown(dist)
    print(
        "postprocessed site/dist "
        f"({mirror_count} markdown mirrors, {html_count} html files, "
        f"{sitemap_count} sitemap files, {sitemap_md_count} sitemap.md)"
    )


if __name__ == "__main__":
    main()
