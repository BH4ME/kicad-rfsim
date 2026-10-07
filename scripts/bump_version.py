#!/usr/bin/env python3
"""Bump RFsim's SemVer in source and PCM metadata.

Usage: bump_version.py patch|minor|major
"""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "plugins" / "version.py"
METADATA_FILE = ROOT / "metadata.json"


def read_version():
    match = re.search(r'(?m)^VERSION\s*=\s*"(\d+)\.(\d+)\.(\d+)"\s*$',
                      VERSION_FILE.read_text())
    if not match:
        raise SystemExit("Cannot find a SemVer in plugins/version.py")
    return tuple(map(int, match.groups()))


def bumped(version, level):
    major, minor, patch = version
    if level == "major":
        return major + 1, 0, 0
    if level == "minor":
        return major, minor + 1, 0
    return major, minor, patch + 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("level", choices=("patch", "minor", "major"))
    args = parser.parse_args()
    old = read_version()
    new = bumped(old, args.level)
    value = "%d.%d.%d" % new
    source = VERSION_FILE.read_text()
    source = re.sub(r'(?m)^VERSION\s*=\s*"[^"]+"\s*$',
                    'VERSION = "' + value + '"', source, count=1)
    VERSION_FILE.write_text(source)
    metadata = json.loads(METADATA_FILE.read_text())
    metadata["versions"][0]["version"] = value
    METADATA_FILE.write_text(json.dumps(metadata, indent=4) + "\n")
    print("%s -> %s" % (".".join(map(str, old)), value))


if __name__ == "__main__":
    main()
