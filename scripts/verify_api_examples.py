#!/usr/bin/env python3
"""Run every example in scripts/api-examples.json against real clients.

The examples are hand-written, so nothing in the site build can prove they
work. This script can: it serves a small page on localhost:3000, then runs
each example in JavaScript, Python, and Java and reports the ones that throw.

It needs a checkout of VibiumDev/vibium with the clients built
(`make build build-java python-venv` there):

    python3 scripts/verify_api_examples.py --vibium ~/Projects/vibium

Run it after editing the examples file, and when an API change lands.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

EXAMPLES = Path(__file__).resolve().parent / "api-examples.json"
BASE = "http://localhost:3000"

PAGE = b"""<!doctype html><title>Demo</title><h1>Welcome</h1>
<nav><a href="/">Home</a> <a href="/next">Next</a> <a href="/file">Download</a></nav>
<label for="email">Email</label><input id="email">
<label for="country">Country</label>
<select id="country"><option value="us">US</option><option value="de">DE</option></select>
<input type="checkbox" aria-label="Remember me">
<button onclick="document.getElementById('out').textContent='submitted'">Submit</button>
<button>Menu</button>
<button onclick="fetch('/api/users')">Users</button>
<div id="out"></div><script>console.log('page ready')</script>"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        headers = {"Content-Type": "text/html"}
        body = PAGE
        if self.path == "/api/users":
            headers, body = {"Content-Type": "application/json"}, b'[{"name": "Alice"}]'
        elif self.path == "/file":
            headers = {
                "Content-Type": "text/plain",
                "Content-Disposition": 'attachment; filename="hello.txt"',
            }
            body = b"hello world"
        elif self.path == "/next":
            body = b"<!doctype html><title>Next</title><h1>Next page</h1>"
        self.send_response(200)
        for name, value in headers.items():
            self.send_header(name, value)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


# Examples that create the browser and page run first and stay in scope;
# stop runs last. Everything else starts from a fresh load of the page.
SETUP = ("1", "2")
LAST = ("3", "6")
# What must happen before an example makes sense, per language.
BEFORE = {
    "11": {  # back(): needs history
        "javascript": f"await vibe.go('{BASE}/next')",
        "python": f'vibe.go("{BASE}/next")',
        "java": f'vibe.go("{BASE}/next");',
    },
    "28": {  # waitForURL(): something has to navigate
        "javascript": "await vibe.find({ role: 'link', text: 'Next' }).click()",
        "python": 'vibe.find(role="link", text="Next").click()',
        "java": 'vibe.find(new SelectorOptions().role("link").text("Next")).click();',
    },
}


def ordered(examples: dict) -> list[str]:
    middle = [i for i in examples if i not in SETUP + LAST]
    return [*SETUP, *middle, *LAST]


def javascript(examples: dict, repo: Path) -> str:
    lines = [
        "import fs from 'node:fs'",
        f"const {{ browser }} = await import('{repo}/clients/javascript/dist/index.mjs')",
    ]
    for i in ordered(examples):
        code = examples[i]["javascript"]
        if i in SETUP:
            lines.append(code)
            continue
        before = BEFORE.get(i, {}).get("javascript", "")
        reset = "" if i in LAST else f"await vibe.go('{BASE}'); "
        lines.append(
            f"try {{ {reset}{before}; {{ {code} }} console.log('ok {i}') }} "
            f"catch (e) {{ console.log('FAIL {i}: ' + String(e.message).slice(0, 120)) }}"
        )
    return "\n".join(lines) + "\n"


def python(examples: dict) -> str:
    lines = ["from pathlib import Path", "from vibium import browser"]
    for i in ordered(examples):
        code = examples[i]["python"]
        if i in SETUP:
            lines.append(code)
            continue
        before = BEFORE.get(i, {}).get("python", "pass")
        reset = "pass" if i in LAST else f'vibe.go("{BASE}")'
        lines += [
            "try:",
            f"    {reset}",
            f"    {before}",
            f"    {code}",
            f"    print('ok {i}')",
            "except Exception as e:",
            f"    print('FAIL {i}: ' + str(e)[:120])",
        ]
    return "\n".join(lines) + "\n"


def java(examples: dict) -> str:
    lines = [
        "import com.vibium.*;",
        "import com.vibium.types.*;",
        "import java.nio.file.Files;",
        "import java.nio.file.Path;",
        "import java.util.List;",
        "public class Examples {",
        "    public static void main(String[] args) throws Exception {",
    ]
    for i in ordered(examples):
        code = examples[i]["java"]
        if i in SETUP:
            # `Page` is ambiguous between the imports only by name, not here.
            lines.append(f"        {code.replace('Page vibe', 'com.vibium.Page vibe')}")
            continue
        before = BEFORE.get(i, {}).get("java", "")
        reset = "" if i in LAST else f'vibe.go("{BASE}");'
        code = code.replace("Page second", "com.vibium.Page second")
        lines.append(
            f"        try {{ {reset} {before} {{ {code} }} System.out.println(\"ok {i}\"); }} "
            f"catch (Exception e) {{ System.out.println(\"FAIL {i}: \" + e.getMessage()); }}"
        )
    lines += ["        System.exit(0);", "    }", "}"]
    return "\n".join(lines) + "\n"


def report(language: str, output: str, examples: dict) -> int:
    passed = {line.split()[1] for line in output.splitlines() if line.startswith("ok ")}
    failed = [line for line in output.splitlines() if line.startswith("FAIL ")]
    expected = set(examples) - set(SETUP)
    missing = sorted(expected - passed - {f.split()[1].rstrip(":") for f in failed}, key=int)
    print(f"{language}: {len(passed)} of {len(expected)} examples ran")
    for line in failed:
        print("  " + line)
    if missing:
        print(f"  no result for: {', '.join(missing)}")
        print("  " + "\n  ".join(output.strip().splitlines()[-4:]))
    return len(failed) + len(missing)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--vibium", type=Path, required=True, help="checkout of VibiumDev/vibium with built clients")
    args = parser.parse_args()
    repo = args.vibium.expanduser().resolve()
    # The published examples name example.com; run them against the local page.
    examples = json.loads(EXAMPLES.read_text().replace("https://example.com", BASE))

    server = HTTPServer(("localhost", 3000), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    env = dict(os.environ, VIBIUM_BIN_PATH=str(repo / "clicker" / "bin" / "vibium"))
    problems = 0

    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)

        (work / "examples.mjs").write_text(javascript(examples, repo))
        run = subprocess.run(["node", "examples.mjs"], cwd=work, env=env, capture_output=True, text=True, timeout=600)
        problems += report("javascript", run.stdout + run.stderr, examples)

        (work / "examples.py").write_text(python(examples))
        interpreter = repo / "clients" / "python" / ".venv" / "bin" / "python"
        run = subprocess.run([str(interpreter), "examples.py"], cwd=work, env=env, capture_output=True, text=True, timeout=600)
        problems += report("python", run.stdout + run.stderr, examples)

        (work / "Examples.java").write_text(java(examples))
        gson = next(Path.home().glob(".gradle/**/gson-*.jar"), None)
        classpath = os.pathsep.join(
            [str(repo / "clients" / "java" / "build" / "classes" / "java" / "main"), str(gson or "")]
        )
        build = subprocess.run(["javac", "-cp", classpath, "-d", ".", "Examples.java"], cwd=work, capture_output=True, text=True)
        if build.returncode:
            print("java: does not compile\n" + build.stderr[-1500:])
            problems += 1
        else:
            run = subprocess.run(
                ["java", "-cp", f".{os.pathsep}{classpath}", "Examples"],
                cwd=work, env=env, capture_output=True, text=True, timeout=600,
            )
            problems += report("java", run.stdout + run.stderr, examples)

    server.shutdown()
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
