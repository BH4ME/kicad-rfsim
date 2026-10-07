# Changelog

## 1.3.0 - 2026-10-07

- Add macOS support for KiCad 10 on Intel and Apple Silicon.
- Discover macOS Python, Homebrew openEMS paths and `venv/bin/python3`.
- Pass native library paths into the solver subprocess and report dynamic
  library import failures.
- Add macOS installation and diagnostic scripts.
- Keep Windows and Linux runtime discovery working.

Version policy: patch releases (`1.3.x`) fix bugs; minor releases (`1.x.0`)
add compatible features; major releases change public behavior or formats.
