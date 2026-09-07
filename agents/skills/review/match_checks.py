#!/usr/bin/env python3
"""Match a diff's changed files against the review checks that apply to them.

Prints each triggered check's path and its `applies-when` text. It deliberately does
not print check bodies; the reviewer reads the files it lists.

Usage:
    match_checks.py                  # working tree against HEAD
    match_checks.py HEAD~1           # a single commit
    match_checks.py main...HEAD      # a branch
    gh pr diff 123 | match_checks.py # a unified diff on stdin
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_CHECKS_DIR = Path(__file__).resolve().parent / "checks"

# "diff --git a/old b/new", with optional quoting around either path.
DIFF_GIT_RE = re.compile(r'^diff --git "?a/(.+?)"? "?b/(.+?)"?$')
# Fallback for diffs that lack the "diff --git" header.
DIFF_PATH_RE = re.compile(r'^(?:---|\+\+\+) "?(?:[ab]/)?(.+?)"?$')


def changed_files_from_diff(text):
    paths = set()
    for line in text.splitlines():
        m = DIFF_GIT_RE.match(line)
        if m:
            paths.update(m.groups())
            continue
        m = DIFF_PATH_RE.match(line)
        if m and m.group(1) != "/dev/null":
            paths.add(m.group(1))
    return sorted(paths)


def changed_files_from_git(revs):
    cmd = ["git", "diff", "--name-only", "--find-renames", *revs]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except FileNotFoundError:
        sys.exit("error: git not found on PATH")
    except subprocess.CalledProcessError as exc:
        sys.exit(f"error: {' '.join(cmd)} failed:\n{exc.stderr.strip()}")
    return sorted(p for p in out.splitlines() if p)


def parse_check(path):
    """Return (triggers, applies_when) from a check's YAML-style header."""
    lines = path.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        print(f"warning: {path} has no header, skipping", file=sys.stderr)
        return None
    triggers, applies_when = [], ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        key, sep, value = line.partition(":")
        if not sep:
            continue
        key, value = key.strip(), value.strip()
        if key == "triggers":
            triggers.extend(t.strip() for t in value.split(",") if t.strip())
        elif key == "applies-when":
            applies_when = value
    else:
        print(f"warning: {path} header is unterminated, skipping", file=sys.stderr)
        return None
    if not triggers:
        print(f"warning: {path} declares no triggers, skipping", file=sys.stderr)
        return None
    return triggers, applies_when


def display_path(path):
    """Prefer a cwd-relative path so the reviewer can open it directly."""
    try:
        return str(path.relative_to(Path.cwd()))
    except ValueError:
        return str(path)


def match(checks_dir, files):
    results = []
    for path in sorted(checks_dir.glob("*.md")):
        parsed = parse_check(path)
        if parsed is None:
            continue
        triggers, applies_when = parsed
        matched = set()
        for pattern in triggers:
            try:
                rx = re.compile(pattern)
            except re.error as exc:
                print(f"warning: {path}: bad regex {pattern!r} ({exc})", file=sys.stderr)
                continue
            matched.update(f for f in files if rx.search(f))
        if matched:
            results.append({
                "check": display_path(path),
                "applies_when": applies_when,
                "matched_files": sorted(matched),
            })
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("revs", nargs="*",
                    help="git revision or range; omit to diff the working tree "
                         "against HEAD, or pipe a unified diff on stdin")
    ap.add_argument("--checks-dir", type=Path, default=DEFAULT_CHECKS_DIR)
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    if not args.checks_dir.is_dir():
        sys.exit(f"error: checks directory not found: {args.checks_dir}")

    if not args.revs and not sys.stdin.isatty():
        files = changed_files_from_diff(sys.stdin.read())
    else:
        files = changed_files_from_git(args.revs or ["HEAD"])

    results = match(args.checks_dir, files)

    if args.json:
        print(json.dumps({"changed_files": files, "triggered": results}, indent=2))
        return

    if not files:
        print("No changed files found. Check the revision range.")
        return
    if not results:
        print(f"{len(files)} changed file(s), no checks triggered.")
        return

    print(f"{len(files)} changed file(s), {len(results)} check(s) triggered.\n")
    for r in results:
        print(r["check"])
        print(f"  applies-when: {r['applies_when']}")
        print(f"  matched: {', '.join(r['matched_files'])}\n")


if __name__ == "__main__":
    main()
