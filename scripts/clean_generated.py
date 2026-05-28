#!/usr/bin/env python3
"""Remove generated docs-site outputs listed in a manifest."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

SKIP_DIRS = {".git", ".jj", ".pnpm-store", "node_modules"}


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def manifest_paths(root: Path, manifest: Path) -> list[Path]:
    paths: list[Path] = []
    lines = manifest.read_text(encoding="utf-8").splitlines()
    for lineno, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        path = Path(line)
        if path.is_absolute() or ".." in path.parts:
            raise SystemExit(
                f"{manifest}: invalid cleanup path on line {lineno}: {line}"
            )
        paths.append(root / path)
    return paths


def remove_path(path: Path) -> bool:
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
        return True
    if path.exists() or path.is_symlink():
        path.unlink()
        return True
    return False


def ds_store_paths(root: Path) -> list[Path]:
    found: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [name for name in dirnames if name not in SKIP_DIRS]
        if ".DS_Store" in filenames:
            found.append(Path(dirpath) / ".DS_Store")
    return found


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: clean_generated.py MANIFEST")

    root = repo_root()
    manifest = (root / sys.argv[1]).resolve()
    removed = 0

    for path in manifest_paths(root, manifest):
        removed += int(remove_path(path))

    for path in ds_store_paths(root):
        removed += int(remove_path(path))

    print(f"removed {removed} generated or OS metadata path(s)")


if __name__ == "__main__":
    main()
