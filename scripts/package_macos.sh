#!/bin/bash
# Build a versioned source package suitable for manual KiCad installation.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VERSION="$(python3 -c 'import pathlib; t=pathlib.Path("plugins/version.py").read_text(); print(next(x.split(chr(34))[1] for x in t.splitlines() if x.startswith("VERSION")))')"
OUT="${1:-$ROOT/dist/rfsim_v${VERSION}_macos.zip}"
mkdir -p "$(dirname "$OUT")"
STAGE="$(mktemp -d "${TMPDIR:-/tmp}/rfsim-package.XXXXXX")"
trap 'rm -rf "$STAGE"' EXIT
mkdir -p "$STAGE/plugins"
rsync -a --exclude '__pycache__' --exclude '*.pyc' \
  "$ROOT/plugins/" "$STAGE/plugins/"
cp "$ROOT/metadata.json" "$ROOT/LICENSE" "$ROOT/README.md" "$ROOT/CHANGELOG.md" "$STAGE/"
(cd "$STAGE" && zip -qr "$OUT" .)
echo "$OUT"
