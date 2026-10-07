# Changelog

## 1.3.1 - 2026-10-07

- Make Homebrew dependency downloads use a temporary HTTP/1.1 curl setting
  when no user setting is present, avoiding intermittent GHCR HTTP/2 resets.

## 1.3.0 - 2026-10-07

- Add macOS support for KiCad 10 on Intel and Apple Silicon.
- Discover macOS Python, Homebrew openEMS paths and `venv/bin/python3`.
- Pass native library paths into the solver subprocess and report dynamic
  library import failures.
- Add macOS installation and diagnostic scripts.
- Keep Windows and Linux runtime discovery working.

Version policy: patch releases (`1.3.x`) fix bugs; minor releases (`1.x.0`)
add compatible features; major releases change public behavior or formats.
