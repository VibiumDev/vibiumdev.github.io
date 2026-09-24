#!/usr/bin/env python3
"""Generate the command reference from the vibium binaries.

Runs `vibium commands` and per-command `--help` on two binaries — the latest
stable npm release and the latest nightly GitHub prerelease — and emits one
Starlight page per top-level command under docs/commands/, plus
docs/commands/index.md and docs/nightly.md.

Commands or flags present only in the nightly binary are marked "Nightly".
Hand-written prose for a command lives in docs/commands/_prose/<name>.md and
is appended verbatim to the generated page (Astro ignores the _prose
directory itself because of the leading underscore).

Usage:
    python3 scripts/gen_command_reference.py
    python3 scripts/gen_command_reference.py --stable-bin PATH --nightly-bin PATH

Without --stable-bin, the script installs vibium@latest from npm into the
work dir. Without --nightly-bin, it downloads the newest nightly-* prerelease
binary for this platform from GitHub. Pages embed no version strings, so the
output only changes when commands or flags actually change.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import stat
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMANDS_DIR = REPO_ROOT / "docs" / "commands"
PROSE_DIR = COMMANDS_DIR / "_prose"
NIGHTLY_PAGE = REPO_ROOT / "docs" / "nightly.md"
WORK_DIR = REPO_ROOT / ".cache" / "reference"

# Debug utilities and cobra built-ins that should not appear in the docs.
EXCLUDED = {"bidi-test", "launch-test", "ws-test", "completion", "help"}

NIGHTLY_NOTE = (
    "> **Nightly only.** This command is in the nightly builds but not yet "
    "in the latest npm release. See [What's in Nightly](../nightly.md)."
)


def run(cmd: list[str], **kwargs) -> str:
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=120, **kwargs
    )
    if result.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd)} failed:\n{result.stderr}")
    return result.stdout


# --- binary acquisition -----------------------------------------------------

def npm_stable_binary(work: Path) -> Path:
    prefix = work / "stable"
    marker = prefix / "node_modules" / ".bin" / "vibium"
    latest = run(["npm", "view", "vibium", "dist-tags.latest"]).strip()
    stamp = prefix / "version.txt"
    if not (marker.exists() and stamp.exists() and stamp.read_text() == latest):
        shutil.rmtree(prefix, ignore_errors=True)
        prefix.mkdir(parents=True)
        env = dict(os.environ, VIBIUM_SKIP_BROWSER_DOWNLOAD="1")
        run(
            ["npm", "install", "--prefix", str(prefix), f"vibium@{latest}"],
            env=env,
        )
        stamp.write_text(latest)
    print(f"stable: vibium@{latest}")
    return marker


def gh_json(url: str):
    req = urllib.request.Request(
        url, headers={"Accept": "application/vnd.github+json"}
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def nightly_asset_name() -> str:
    goos = {"darwin": "darwin", "linux": "linux", "win32": "windows"}[
        sys.platform if sys.platform != "cygwin" else "win32"
    ]
    goarch = {"x86_64": "amd64", "amd64": "amd64", "arm64": "arm64",
              "aarch64": "arm64"}[platform.machine().lower()]
    name = f"vibium-{goos}-{goarch}"
    return name + (".exe" if goos == "windows" else "")


def nightly_binary(work: Path) -> tuple[Path, str]:
    releases = gh_json(
        "https://api.github.com/repos/VibiumDev/vibium/releases?per_page=15"
    )
    asset_name = nightly_asset_name()
    for release in releases:
        if not release.get("prerelease"):
            continue
        if not release["tag_name"].startswith("nightly-"):
            continue
        assets = {a["name"]: a for a in release.get("assets", [])}
        if asset_name in assets:
            tag = release["tag_name"]
            dest = work / "nightly" / tag / asset_name
            if not dest.exists():
                shutil.rmtree(work / "nightly", ignore_errors=True)
                dest.parent.mkdir(parents=True)
                url = assets[asset_name]["browser_download_url"]
                print(f"nightly: downloading {tag} ({asset_name})")
                urllib.request.urlretrieve(url, dest)
                dest.chmod(dest.stat().st_mode | stat.S_IEXEC)
            print(f"nightly: {tag}")
            return dest, tag
    raise RuntimeError(f"no nightly release with asset {asset_name} found")


# --- help harvesting --------------------------------------------------------

class Help:
    """Parsed cobra --help output for one command path."""

    def __init__(self, text: str, binary_name: str = "clicker"):
        # Cobra prints argv[0]'s basename (e.g. vibium-darwin-arm64) in
        # usage lines; normalize it and the internal "clicker" name.
        self.text = text.replace(binary_name, "vibium").replace(
            "clicker", "vibium"
        )
        lines = self.text.splitlines()
        self.short = lines[0].strip() if lines else ""
        self.usage = self._section("Usage:")
        self.examples = self._section("Examples:")
        self.flags = self._section("Flags:")
        self.subcommands = self._section("Available Commands:")

    def _section(self, header: str) -> str:
        lines = self.text.splitlines()
        out: list[str] = []
        collecting = False
        for line in lines:
            if line.rstrip() == header:
                collecting = True
                continue
            if collecting:
                if line and not line[0].isspace():
                    break
                out.append(line)
        while out and not out[-1].strip():
            out.pop()
        return "\n".join(self._dedent(out))

    @staticmethod
    def _dedent(lines: list[str]) -> list[str]:
        indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
        cut = min(indents) if indents else 0
        return [l[cut:] if l.strip() else "" for l in lines]

    def flag_names(self) -> set[str]:
        return set(re.findall(r"--[a-z][a-z0-9-]*", self.flags)) - {"--help"}

    def public_flags(self) -> str:
        kept = [
            l for l in self.flags.splitlines()
            if not re.match(r"\s*-h, --help\b", l)
        ]
        return "\n".join(kept).strip("\n")


class Binary:
    """Walks the command tree via recursive --help parsing.

    (The `vibium commands` JSON listing would be simpler, but it does not
    exist in every release yet; the help walk works on any cobra binary.)
    """

    def __init__(self, path: Path):
        self.path = path
        self._help: dict[str, Help] = {}
        self.paths: list[str] = []
        self._walk("")
        self.paths.sort()
        self.top_level = sorted({c.split()[0] for c in self.paths})

    def _walk(self, prefix: str) -> None:
        for line in self.help(prefix).subcommands.splitlines():
            name = line.split()[0] if line.split() else ""
            if not name or (not prefix and name in EXCLUDED):
                continue
            path = f"{prefix} {name}".strip()
            self.paths.append(path)
            self._walk(path)

    def help(self, command_path: str = "") -> Help:
        if command_path not in self._help:
            # `vibium help <cmd>` rather than `<cmd> --help`: older releases
            # error on --help for commands that disable flag parsing.
            args = [str(self.path), "help"] + command_path.split()
            self._help[command_path] = Help(run(args), self.path.name)
        return self._help[command_path]


# --- page emission ----------------------------------------------------------

def page_name(top: str) -> str:
    return f"{top}.md"


def prose_for(name: str) -> str:
    prose = PROSE_DIR / f"{name}.md"
    if prose.exists():
        return prose.read_text().strip()
    return ""


def code_block(text: str, lang: str = "") -> str:
    return f"```{lang}\n{text}\n```"


def sentence(short: str) -> str:
    return short if short.endswith(".") else short + "."


def command_section(
    path: str, nightly: Binary, stable_paths: set[str],
    stable: Binary, heading_level: int,
) -> list[str]:
    """Synopsis/flags/examples for one command path, with nightly markers."""
    help_ = nightly.help(path)
    out: list[str] = []
    if path not in stable_paths:
        out.append(NIGHTLY_NOTE)
    out.append(code_block(help_.usage))
    flags = help_.public_flags()
    if flags:
        h = "#" * heading_level
        out.append(f"{h} Flags")
        out.append(code_block(flags))
        if path in stable_paths:
            new = help_.flag_names() - stable.help(path).flag_names()
            if new:
                pretty = ", ".join(f"`{f}`" for f in sorted(new))
                out.append(
                    f"New in nightly (not yet in the npm release): {pretty}"
                )
    return out


def emit_command_page(
    top: str, nightly: Binary, stable: Binary, stable_paths: set[str]
) -> str:
    help_ = nightly.help(top)
    nightly_only = top not in stable_paths
    front = [f"title: vibium {top}"]
    if nightly_only:
        front.append("sidebar:\n  badge: Nightly")
    parts = ["---\n" + "\n".join(front) + "\n---", "", sentence(help_.short), ""]
    parts.append("## Synopsis")
    parts.extend(command_section(top, nightly, stable_paths, stable, 2))

    sub_paths = [
        p for p in nightly.paths if p.startswith(top + " ")
    ]
    if sub_paths:
        parts.append("## Subcommands")
        for sub in sub_paths:
            sub_help = nightly.help(sub)
            parts.append(f"### vibium {sub}")
            parts.append(sentence(sub_help.short))
            parts.extend(
                command_section(sub, nightly, stable_paths, stable, 4)
            )
            if sub_help.examples:
                parts.append(code_block(sub_help.examples, "sh"))

    prose = prose_for(top)
    if prose:
        parts.append(prose)
    elif help_.examples:
        parts.append("## Examples")
        parts.append(code_block(help_.examples, "sh"))

    return "\n\n".join(p for p in parts if p != "") + "\n"


def emit_index(nightly: Binary, stable: Binary, stable_tops: set[str]) -> str:
    parts = ["---\ntitle: Command Reference\nsidebar:\n  order: 0\n---"]
    prose = prose_for("index")
    if prose:
        parts.append(prose)
    rows = ["| Command | Description |", "| ------- | ----------- |"]
    for top in nightly.top_level:
        desc = nightly.help(top).short
        badge = " **(nightly)**" if top not in stable_tops else ""
        rows.append(f"| [`vibium {top}`]({top}.md){badge} | {desc} |")
    parts.append("\n".join(rows))
    parts.append(
        "Commands marked **(nightly)** are not yet in the latest npm "
        "release; see [What's in Nightly](../nightly.md)."
    )
    parts.append("## Global flags")
    parts.append(
        "Every command accepts these flags in addition to its own:"
    )
    root_flags = nightly.help("").public_flags()
    parts.append(code_block(root_flags))
    return "\n\n".join(parts) + "\n"


def emit_nightly_page(
    nightly: Binary, stable: Binary,
    stable_paths: set[str], stable_version: str,
) -> str:
    new_commands = [p for p in nightly.paths if p not in stable_paths]
    new_flags: list[tuple[str, list[str]]] = []
    for path in nightly.paths:
        if path not in stable_paths:
            continue
        added = nightly.help(path).flag_names() - stable.help(path).flag_names()
        if added:
            new_flags.append((path, sorted(added)))

    parts = [
        "---\ntitle: What's in Nightly\n---",
        "Vibium publishes automated nightly builds from `main` as GitHub "
        "prereleases, ahead of the next npm release. This page is "
        "regenerated automatically by diffing the two binaries: everything "
        f"listed here is in the current nightly but **not** in "
        f"`vibium@{stable_version}`, the latest npm release.",
        "Get a nightly from the "
        "[releases page](https://github.com/VibiumDev/vibium/releases) — "
        "the `nightly-*` prereleases carry standalone binaries plus npm "
        "and Python packages. Nightlies are automated and unsupported.",
    ]

    if not new_commands and not new_flags:
        parts.append(
            "## No differences\n\nThe current nightly has no new commands "
            "or flags compared to the npm release."
        )
        return "\n\n".join(parts) + "\n"

    if new_commands:
        parts.append("## New commands")
        rows = ["| Command | Description |", "| ------- | ----------- |"]
        for path in new_commands:
            top = path.split()[0]
            desc = nightly.help(path).short
            rows.append(f"| [`vibium {path}`](commands/{top}.md) | {desc} |")
        parts.append("\n".join(rows))

    if new_flags:
        parts.append("## New flags on existing commands")
        rows = ["| Command | New flags |", "| ------- | --------- |"]
        for path, flags in new_flags:
            top = path.split()[0]
            pretty = ", ".join(f"`{f}`" for f in flags)
            rows.append(f"| [`vibium {path}`](commands/{top}.md) | {pretty} |")
        parts.append("\n".join(rows))

    return "\n\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stable-bin", type=Path)
    parser.add_argument("--nightly-bin", type=Path)
    parser.add_argument("--workdir", type=Path, default=WORK_DIR)
    args = parser.parse_args()

    args.workdir.mkdir(parents=True, exist_ok=True)
    stable_bin = args.stable_bin or npm_stable_binary(args.workdir)
    if args.nightly_bin:
        nightly_bin = args.nightly_bin
    else:
        nightly_bin, _ = nightly_binary(args.workdir)

    stable = Binary(stable_bin)
    nightly = Binary(nightly_bin)
    stable_version = run([str(stable_bin), "version"]).split()[-1].lstrip("v")

    stable_paths = set(stable.paths)
    dropped = [p for p in stable.paths if p not in set(nightly.paths)]
    if dropped:
        print(f"WARNING: in stable but not nightly (kept out of docs): {dropped}")

    COMMANDS_DIR.mkdir(parents=True, exist_ok=True)
    wanted = {page_name(t) for t in nightly.top_level} | {"index.md"}
    for old in COMMANDS_DIR.glob("*.md"):
        if old.name not in wanted:
            print(f"removing stale page {old.name}")
            old.unlink()

    for top in nightly.top_level:
        page = COMMANDS_DIR / page_name(top)
        page.write_text(emit_command_page(top, nightly, stable, stable_paths))
    (COMMANDS_DIR / "index.md").write_text(
        emit_index(nightly, stable, {p.split()[0] for p in stable.paths})
    )
    NIGHTLY_PAGE.write_text(
        emit_nightly_page(nightly, stable, stable_paths, stable_version)
    )
    print(
        f"wrote {len(nightly.top_level)} command pages, index.md, "
        f"and docs/nightly.md"
    )


if __name__ == "__main__":
    main()
