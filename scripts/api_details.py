#!/usr/bin/env python3
"""Typed signatures and doc comments for the client libraries.

The API spec (docs/reference/api.md upstream) names every method. This
module supplies what the spec leaves out: parameter names, types, defaults,
return types, and the doc comment, read from the artifacts a nightly
release publishes:

  JavaScript  dist/index.d.ts inside the npm tarball
  Python      the sync_api and async_api sources inside the wheel
  Java        com/vibium/**/*.java inside the sources jar

Nothing is installed or executed; the files are parsed as text.
"""
from __future__ import annotations

import ast
import io
import json
import re
import tarfile
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

RELEASE_URL = "https://github.com/VibiumDev/vibium/releases/download/{tag}/{name}"

# The receiver a spec cell starts with, and the classes that may define it.
RECEIVERS: dict[str, list[str]] = {
    "browser": ["Browser", "browser", "_BrowserLauncher"],
    "Vibium": ["Vibium"],
    "page": ["Page"],
    "page.capture()": ["Capture"],
    "page.capture": ["Page.capture", "_SyncCaptureNamespace", "_CaptureNamespace"],
    "el": ["Element"],
    "context": ["BrowserContext"],
    "keyboard": ["Keyboard"],
    "mouse": ["Mouse"],
    "touch": ["Touch"],
    "clock": ["Clock"],
    "recording": ["Recording"],
    "route": ["Route"],
    "dialog": ["Dialog"],
    "download": ["Download", "SyncDownload"],
    "request": ["Request", "_SyncRequestData"],
    "response": ["Response", "_SyncResponseData"],
    "message": ["ConsoleMessage"],
    "socket": ["WebSocketInfo"],
}

CELL_RE = re.compile(r"^`?([A-Za-z]+(?:\.capture(?:\(\))?)?)\.([A-Za-z_]\w*)")
TYPE_NAME_RE = re.compile(r"\b[A-Z][A-Za-z0-9]*(?:\$\d+)?")


@dataclass
class Member:
    signatures: list[str] = field(default_factory=list)
    doc: str = ""


@dataclass
class Details:
    """One language: its classes' public members and its named types."""

    fence: str
    classes: dict[str, dict[str, Member]] = field(default_factory=dict)
    types: dict[str, str] = field(default_factory=dict)

    def lookup(self, cell: str) -> Member | None:
        match = CELL_RE.match(cell)
        if not match:
            return None
        receiver, name = match.groups()
        for cls in RECEIVERS.get(receiver, []):
            member = self.classes.get(cls, {}).get(name)
            if member:
                return member
        return None

    def referenced_types(self, signatures: list[str]) -> list[str]:
        """Named types the signatures mention, plus the types those mention."""
        found: list[str] = []
        queue = list(signatures)
        while queue:
            for name in TYPE_NAME_RE.findall(queue.pop()):
                if name in self.types and name not in found:
                    found.append(name)
                    queue.append(self.types[name])
        return sorted(found)


# --- JavaScript --------------------------------------------------------------

JS_MEMBER_RE = re.compile(
    r"^(?:static\s+)?(?:readonly\s+)?(?:get\s+|set\s+)?([A-Za-z_$][\w$]*)\??\s*[(:<]"
)


def clean_block_comment(lines: list[str]) -> str:
    """A /** ... */ comment as one line of Markdown-safe prose."""
    words: list[str] = []
    for line in lines:
        line = line.strip()
        line = re.sub(r"^/\*\*|\*/$", "", line).strip()
        line = re.sub(r"^\*\s?", "", line)
        if line:
            words.append(line)
    text = re.sub(r"\{@(?:link|code)\s+#?([^}]+)\}", r"`\1`", " ".join(words))
    return escape_markdown(" ".join(text.split()))


def escape_markdown(text: str) -> str:
    """Escape what Markdown would read as a link, tag, or emphasis, outside code spans."""
    parts = text.split("`")
    for i in range(0, len(parts), 2):
        parts[i] = re.sub(r"([\[\]<>*])", r"\\\1", parts[i])
    return "`".join(parts)


def parse_dts(text: str) -> Details:
    details = Details(fence="ts")
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        head = re.match(
            r"^(?:declare (?:abstract )?class (\w+)|declare const (\w+): \{|interface ([\w$]+))",
            line,
        )
        alias = re.match(r"^type ([\w$]+)", line)
        if alias:
            block = [line]
            while not block[-1].rstrip().endswith(";") and i + 1 < len(lines):
                i += 1
                block.append(lines[i])
            details.types[alias.group(1)] = "\n".join(block)
            i += 1
            continue
        if not head:
            i += 1
            continue
        end = i + 1
        while end < len(lines) and not re.match(r"^\};?$", lines[end]):
            end += 1
        body = lines[i + 1 : end]
        cls, const, interface = head.groups()
        if interface:
            details.types[interface] = "\n".join(lines[i : end + 1])
        else:
            nested: dict[str, dict[str, Member]] = {}
            details.classes[cls or const] = js_members(body, nested)
            for name, members in nested.items():
                details.classes[f"{cls or const}.{name}"] = members
        i = end + 1
    return details


def js_members(
    body: list[str], nested: dict[str, dict[str, Member]] | None = None
) -> dict[str, Member]:
    """Public members of a class body. An inline object type (Page's capture
    namespace) also lands in `nested` under its property name."""
    members: dict[str, Member] = {}
    doc: list[str] = []
    i = 0
    while i < len(body):
        stripped = body[i].strip()
        if stripped.startswith("/**"):
            doc = [stripped]
            while not doc[-1].endswith("*/") and i + 1 < len(body):
                i += 1
                doc.append(body[i].strip())
            i += 1
            continue
        decl = [body[i]]
        depth = body[i].count("{") + body[i].count("(") - body[i].count("}") - body[i].count(")")
        while (depth > 0 or not decl[-1].rstrip().endswith(";")) and i + 1 < len(body):
            i += 1
            decl.append(body[i])
            depth += body[i].count("{") + body[i].count("(") - body[i].count("}") - body[i].count(")")
        i += 1
        comment, doc = clean_block_comment(doc) if doc else "", []
        name = JS_MEMBER_RE.match(stripped)
        if (
            not name
            or stripped.startswith(("private", "protected", "constructor", "["))
            or name.group(1).startswith("_")
            or "@internal" in comment
        ):
            continue
        signature = "\n".join(d[4:] if d.startswith("    ") else d for d in decl)
        if nested is not None and len(decl) > 2 and decl[0].rstrip().endswith("{"):
            nested[name.group(1)] = js_members([d[4:] for d in decl[1:-1]])
        member = members.setdefault(name.group(1), Member())
        member.signatures.append(signature)
        member.doc = member.doc or comment
    return members


# --- Python ------------------------------------------------------------------

def split_params(params: str) -> list[str]:
    parts, depth, current = [], 0, ""
    for ch in params:
        depth += ch in "([{"
        depth -= ch in ")]}"
        if ch == "," and depth == 0:
            parts.append(current.strip())
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current.strip())
    return parts


def spaced_default(param: str) -> str:
    """`x: int=1` as `x: int = 1`, the way annotated defaults are written."""
    if ":" not in param:
        return param
    depth = 0
    for i, ch in enumerate(param):
        depth += ch in "([{"
        depth -= ch in ")]}"
        if ch == "=" and depth == 0:
            return f"{param[:i].rstrip()} = {param[i + 1:].lstrip()}"
    return param


def python_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = node.args
    if args.posonlyargs:
        args.posonlyargs = args.posonlyargs[1:]
    elif args.args:
        args.args = args.args[1:]
    parts = [spaced_default(part) for part in split_params(ast.unparse(args))]
    params = ", ".join(parts)
    returns = f" -> {ast.unparse(node.returns)}" if node.returns else ""
    is_property = any(
        isinstance(d, ast.Name) and d.id == "property" for d in node.decorator_list
    )
    if is_property:
        return f"{node.name}{returns.replace(' -> ', ': ')}  # property"
    flat = f"{node.name}({params}){returns}"
    if len(flat) <= 120:
        return flat
    body = "".join(f"    {part},\n" for part in parts)
    return f"{node.name}(\n{body}){returns}"


def python_type(node: ast.ClassDef) -> str | None:
    """A data class as its annotated fields, or None if it has none."""
    fields = [ast.unparse(s) for s in node.body if isinstance(s, ast.AnnAssign)]
    if not fields:
        return None
    bases = ", ".join(ast.unparse(b) for b in node.bases)
    head = f"class {node.name}({bases}):" if bases else f"class {node.name}:"
    return "\n".join([head, *(f"    {f}" for f in fields)])


def parse_python(sources: dict[str, str]) -> Details:
    """`sources` maps a path inside the wheel to its text. sync_api wins."""
    details = Details(fence="python")
    ordered = sorted(sources, key=lambda p: ("/sync_api/" not in p, p))
    for path in ordered:
        for node in ast.parse(sources[path]).body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Subscript):
                for target in node.targets:  # ImageInput = Union[...]
                    if isinstance(target, ast.Name) and target.id[:1].isupper():
                        details.types.setdefault(target.id, ast.unparse(node))
            if not isinstance(node, ast.ClassDef):
                continue
            data = python_type(node)
            if data:
                details.types.setdefault(node.name, data)
            members = details.classes.setdefault(node.name, {})
            for item in node.body:
                if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    continue
                if item.name.startswith("_"):
                    continue
                doc = " ".join((ast.get_docstring(item) or "").split("\n\n")[0].split())
                doc = escape_markdown(doc.replace("``", "`"))
                if item.name in members:
                    # The sync class came first. Its methods often carry no
                    # docstring where the async twin does; same method, so
                    # the async text applies.
                    members[item.name].doc = members[item.name].doc or doc
                    continue
                members[item.name] = Member([python_signature(item)], doc)
    return details


# --- Java --------------------------------------------------------------------

JAVA_METHOD_RE = re.compile(r"^public\s+(?!class|interface|enum|record)[^=;]*?\b(\w+)\s*\(")


def parse_java(sources: dict[str, str]) -> Details:
    details = Details(fence="java")
    for path, text in sorted(sources.items()):
        cls = Path(path).stem
        members: dict[str, Member] = {}
        doc: list[str] = []
        depth = 0
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            stripped = lines[i].strip()
            if depth == 1 and stripped.startswith("/**"):
                doc = [stripped]
                while not doc[-1].endswith("*/") and i + 1 < len(lines):
                    i += 1
                    doc.append(lines[i].strip())
                i += 1
                continue
            method = JAVA_METHOD_RE.match(stripped) if depth == 1 else None
            if method:
                decl = [stripped]
                while "{" not in decl[-1] and not decl[-1].endswith(";") and i + 1 < len(lines):
                    i += 1
                    decl.append(lines[i].strip())
                signature = " ".join(decl).split("{")[0].rstrip(" ;")
                signature = re.sub(r"\s*throws [\w., ]+$", "", signature)
                member = members.setdefault(method.group(1), Member())
                member.signatures.append(signature + ";")
                comment = clean_block_comment(doc) if doc else ""
                member.doc = member.doc or re.split(r"\s@\w+", comment)[0].strip()
                depth += sum(d.count("{") - d.count("}") for d in decl)
            else:
                depth += stripped.count("{") - stripped.count("}")
            if stripped and not stripped.startswith(("@", "/**", "*")):
                doc = []
            i += 1
        details.classes[cls] = members
        if "/types/" in path:
            plumbing = {"toString", "toParams", "equals", "hashCode"}
            public = [
                s for n, m in members.items() if n not in plumbing for s in m.signatures
            ]
            if public:
                details.types[cls] = "\n".join([f"class {cls} {{", *(f"    {s}" for s in public), "}"])
    return details


# --- Artifacts ---------------------------------------------------------------

def download(tag: str, name: str, dest: Path) -> Path:
    target = dest / name
    if not target.exists():
        dest.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(RELEASE_URL.format(tag=tag, name=name), target)
    return target


def load(tag: str, work: Path) -> dict[str, Details]:
    """Details for all three languages from the nightly release `tag`."""
    dest = work / "api" / tag
    manifest = json.loads(download(tag, "manifest.json", dest).read_text())
    npm = download(tag, f"vibium-{manifest['npmVersion']}.tgz", dest)
    wheel = download(tag, f"vibium-{manifest['pythonVersion']}-py3-none-any.whl", dest)
    jar = download(tag, f"vibium-{manifest['mavenVersion']}-sources.jar", dest)

    with tarfile.open(npm) as tar:
        dts = tar.extractfile("package/dist/index.d.ts").read().decode("utf-8")
    with zipfile.ZipFile(wheel) as zf:
        python = {
            n: zf.read(n).decode("utf-8")
            for n in zf.namelist()
            if n.startswith("vibium/") and n.endswith(".py")
        }
    with zipfile.ZipFile(jar) as zf:
        java = {
            n: io.TextIOWrapper(zf.open(n), encoding="utf-8").read()
            for n in zf.namelist()
            if n.startswith("com/vibium/") and n.endswith(".java") and "/internal/" not in n
        }
    return {
        "javascript": parse_dts(dts),
        "python": parse_python(python),
        "java": parse_java(java),
    }
