#!/usr/bin/env python3
"""Verify local KI-Lego release hashes; never installs or contacts a service."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys

def verify(root):
    manifest = root / "references/source.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ValueError("manifest unavailable or invalid: " + str(exc)) from exc
    if not isinstance(data, dict):
        raise ValueError("manifest must be an object")
    if not isinstance(data.get("release"), str) or not re.fullmatch(r"\d+\.\d+\.\d+", data["release"]):
        raise ValueError("manifest release must be a semantic version")
    if not isinstance(data.get("source_commit"), str) or not re.fullmatch(r"[a-f0-9]{40}", data["source_commit"]):
        raise ValueError("manifest source_commit must be a pinned commit")
    files = data.get("files")
    if not isinstance(files, dict) or not files:
        raise ValueError("manifest files must be a nonempty map")
    failures = []
    for name, expected in files.items():
        if not isinstance(name, str):
            raise ValueError("invalid path")
        path = PurePosixPath(name)
        if path.is_absolute() or ".." in path.parts or "\\" in name or not path.parts:
            raise ValueError("unsafe path: " + name)
        target = (root / name).resolve()
        if not target.is_relative_to(root.resolve()):
            raise ValueError("path escapes root: " + name)
        if not isinstance(expected, str) or not re.fullmatch(r"[a-f0-9]{64}", expected):
            raise ValueError("invalid hash for " + name)
        try:
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
        except OSError:
            failures.append(name + ": missing or unreadable")
            continue
        if actual != expected:
            failures.append(name + ": content mismatch")
    if failures:
        raise ValueError("; ".join(failures))
    return data["release"], len(files)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        version, count = verify(args.root)
    except ValueError as exc:
        print("FAIL: " + str(exc), file=sys.stderr)
        return 1
    print(f"OK: KI-Lego {version}; {count} files verified locally. Remote freshness and service access not checked.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
