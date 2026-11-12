#!/usr/bin/env python3
"""Import guides from the main vibium repository into docs/.

scripts/upstream-manifest.json lists the pages. Each one is fetched from
VibiumDev/vibium at the latest nightly tag and rewritten just enough to
live on the site:

  - the leading H1 becomes the frontmatter title
  - the first paragraph becomes the description
  - links to other imported pages (or to their site equivalents, the
    manifest's "aliases") become site links; any other relative link
    becomes a GitHub link
  - relative images become raw GitHub URLs
  - a note names any nightly-only command or MCP tool the page uses, or
    says the page is new or changed since the npm release

The output is committed, like docs/commands/, so builds need no network.
Edit the pages upstream, not here.

Usage:
    python3 scripts/import_upstream_docs.py
    python3 scripts/import_upstream_docs.py --ref main
"""
from __future__ import annotations

import argparse
import json
import posixpath
import re
import urllib.error
import urllib.request
from pathlib import Path

from gen_api_reference import latest_nightly_tag
from gen_command_reference import REPO_ROOT, run

MANIFEST = REPO_ROOT / "scripts" / "upstream-manifest.json"
COMMANDS_JSON = REPO_ROOT / "site" / "public" / "commands.json"
MCP_TOOLS_JSON = REPO_ROOT / "site" / "public" / "mcp-tools.json"
LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")
FENCE_RE = re.compile(r"^(```|~~~)")
BLOCK_START_RE = re.compile(r"^([-*+] |\d+\. |#|>|\||<|!\[)")


def fetch(repo: str, ref: str, path: str) -> str | None:
    url = f"https://raw.githubusercontent.com/{repo}/{ref}/{path}"
    try:
        with urllib.request.urlopen(url) as resp:
            return resp.read().decode("utf-8")
    except urllib.error.HTTPError as err:
        if err.code == 404:
            return None
        raise


def split_title(text: str, src: str) -> tuple[str, str]:
    lines = text.lstrip().splitlines()
    if not lines or not lines[0].startswith("# "):
        raise SystemExit(f"import_upstream_docs: {src} does not start with an H1")
    return lines[0][2:].strip(), "\n".join(lines[1:]).lstrip("\n")


def first_paragraph(body: str) -> str:
    paragraph: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        stripped = line.strip()
        if in_fence or BLOCK_START_RE.match(stripped):
            if paragraph:
                break
            continue
        if not stripped:
            if paragraph and " · " in " ".join(paragraph):
                paragraph = []  # a "Part 1 · Part 2" navigation line, not prose
            elif paragraph:
                break
            continue
        paragraph.append(stripped)
    return describe(" ".join(paragraph))


def describe(text: str, min_len: int = 60, max_len: int = 180) -> str:
    """Whole sentences from the opening paragraph, long enough for a meta description."""
    text = LINK_RE.sub(r"\2", text).replace("`", "").replace("**", "")
    description = ""
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        candidate = f"{description} {sentence}".strip()
        if description and len(candidate) > max_len:
            break
        description = candidate
        if len(description) >= min_len:
            break
    if len(description) > max_len:
        description = description[: max_len - 3].rsplit(" ", 1)[0].rstrip(".,;:") + "..."
    return description


def rewrite_links(body: str, src: str, dest: str, site_paths: dict[str, str], repo: str) -> str:
    """Point relative links at the site where it has the page, else at GitHub."""

    def repl(match: re.Match[str]) -> str:
        bang, label, target = match.groups()
        if target.startswith(("http://", "https://", "#", "mailto:", "/")):
            return match.group(0)
        path, _, anchor = target.partition("#")
        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(src), path))
        anchor = f"#{anchor}" if anchor else ""
        if bang:
            return f"![{label}](https://raw.githubusercontent.com/{repo}/main/{resolved})"
        if resolved not in site_paths and f"{resolved}/README.md" in site_paths:
            resolved = f"{resolved}/README.md"
        if resolved in site_paths:
            relative = posixpath.relpath(site_paths[resolved], posixpath.dirname(dest))
            return f"[{label}]({relative}{anchor})"
        return f"[{label}](https://github.com/{repo}/blob/main/{resolved}{anchor})"

    out: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
        out.append(line if in_fence else LINK_RE.sub(repl, line))
    return "\n".join(out)


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


class NightlyIndex:
    """What only the nightly has, from the generated command and MCP listings."""

    def __init__(self) -> None:
        commands = json.loads(COMMANDS_JSON.read_text())["commands"]
        tools = json.loads(MCP_TOOLS_JSON.read_text())["tools"]
        self.paths = sorted((c["command"] for c in commands), key=len, reverse=True)
        self.new_commands = {c["command"] for c in commands if c["nightlyOnly"]}
        self.new_flags = {c["command"]: c.get("nightlyOnlyFlags", []) for c in commands}
        self.new_tools = [t["name"] for t in tools if t["nightlyOnly"]]

    def used_by(self, text: str) -> list[str]:
        """Nightly-only commands, flags, and MCP tools that a page mentions."""
        found: set[str] = set()
        for match in re.finditer(r"vibium [a-z][^\n`|]*", text):
            invocation = match.group(0)
            path = next(
                (p for p in self.paths if re.match(re.escape(p) + r"(?![\w-])", invocation)),
                None,
            )
            if path is None:
                continue
            if path in self.new_commands:
                found.add(path)
            for flag in self.new_flags[path]:
                if re.search(re.escape(flag) + r"(?![\w-])", invocation):
                    found.add(f"{path} {flag}")
        for tool in self.new_tools:
            if re.search(rf"\b{tool}\b", text):
                found.add(tool)
        return sorted(found)


def release_note(
    used: list[str], stable_text: str | None, text: str, stable_version: str, dest: str
) -> str:
    nightly = posixpath.relpath("docs/nightly.md", posixpath.dirname(dest))
    if used:
        shown = ", ".join(f"`{name}`" for name in used[:6])
        more = f", and {len(used) - 6} more" if len(used) > 6 else ""
        verb = "is" if len(used) == 1 else "are"
        return (
            f"> **Nightly only.** This guide uses {shown}{more}, which {verb} not in "
            f"{stable_version}. See [What's in Nightly]({nightly}).\n\n"
        )
    if stable_text != text:
        when = "added" if stable_text is None else "updated"
        return (
            f"> This guide was {when} after the {stable_version} release, so parts of "
            f"it MAY need a nightly build. See [What's in Nightly]({nightly}).\n\n"
        )
    return ""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", help="upstream ref to import (default: latest nightly tag)")
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text())
    repo = manifest["repo"]
    pages = manifest["pages"]
    site_paths = {**manifest.get("aliases", {}), **{p["src"]: p["dest"] for p in pages}}

    ref = args.ref or latest_nightly_tag()
    stable_version = run(["npm", "view", "vibium", "dist-tags.latest"]).strip()
    print(f"upstream docs: {ref} vs v{stable_version}")
    nightly = NightlyIndex()

    for page in pages:
        src, dest = page["src"], page["dest"]
        text = fetch(repo, ref, src)
        if text is None:
            raise SystemExit(f"import_upstream_docs: {src} not found at {ref}")
        title, body = split_title(text, src)
        title = page.get("title", title)
        description = first_paragraph(body)
        if len(description) < 50:
            description = f"{title}. {description}".strip()
        body = rewrite_links(body, src, dest, site_paths, repo)
        used = nightly.used_by(text)
        note = release_note(
            used, fetch(repo, f"v{stable_version}", src), text, stable_version, dest
        )
        front = ["---", f"title: {yaml_string(title)}"]
        if description:
            front.append(f"description: {yaml_string(description)}")
        sidebar = []
        if dest.endswith("/index.md"):
            sidebar += ["  label: Overview", "  order: 0"]
        if used:
            sidebar.append("  badge: Nightly")
        if sidebar:
            front += ["sidebar:", *sidebar]
        front += [
            f"editUrl: https://github.com/{repo}/edit/main/{src}",
            "---",
            "",
            f"<!-- Imported from {src} in {repo} by scripts/import_upstream_docs.py. Edit it there. -->",
            "",
            "",
        ]
        target = REPO_ROOT / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("\n".join(front) + note + body.rstrip() + "\n", encoding="utf-8")
        print(f"  {src} -> {dest}")
    print(f"imported {len(pages)} pages")


if __name__ == "__main__":
    main()
