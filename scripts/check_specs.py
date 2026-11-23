#!/usr/bin/env python3
"""Fails when a change edits or deletes a published spec, or adds one that does not point to a Primer repo tag.

Usage: check_specs.py <base commit>
"""
import json, pathlib, subprocess, sys

REPOS = {f"https://github.com/primer-io/{name}.git" for name in (
    "primer-sdk-ios", "primer-sdk-3ds-ios", "primer-klarna-sdk-ios",
    "primer-ipay88-sdk-ios", "primer-nol-pay-sdk-ios", "primer-stripe-sdk-ios",
)}

def problems(base):
    diff = subprocess.run(["git", "diff", "--name-status", "--no-renames", base, "HEAD"],
                          capture_output=True, text=True, check=True).stdout
    for line in diff.splitlines():
        status, path = line.split("\t", 1)
        if not path.endswith((".podspec", ".podspec.json")):
            continue
        if status != "A":
            yield f"{path}: published specs must not change ({status})"
            continue
        parts = pathlib.PurePosixPath(path).parts
        if len(parts) != 3 or parts[2] != f"{parts[0]}.podspec.json":
            yield f"{path}: specs belong in <Pod>/<version>/<Pod>.podspec.json"
            continue
        pod, version, _ = parts
        try:
            spec = json.loads(pathlib.Path(path).read_text())
        except ValueError as error:
            yield f"{path}: invalid JSON ({error})"
            continue
        if spec.get("name") != pod or spec.get("version") != version:
            yield f"{path}: name or version does not match the path"
        source = spec.get("source", {})
        if source.get("git") not in REPOS or not source.get("tag"):
            yield f"{path}: source must be a tag in a Primer repo, got {source}"

def main():
    found = list(problems(sys.argv[1]))
    print("\n".join(found) or "All spec changes are fine")
    sys.exit(1 if found else 0)

if __name__ == "__main__":
    main()
