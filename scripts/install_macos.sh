#!/bin/bash
# Install RFsim into the KiCad 10 macOS ActionPlugin directory.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KICAD_VERSION="${KICAD_VERSION:-10.0}"
KICAD_APP="${KICAD_APP:-/Applications/KiCad/KiCad.app}"
KICAD_PYTHON="${KICAD_PYTHON:-$KICAD_APP/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3.9}"
PLUGIN_DIR="${KICAD_PLUGIN_DIR:-$HOME/Documents/KiCad/$KICAD_VERSION/scripting/plugins/rfsim}"
OPENEMS_PREFIX="${OPENEMS_PREFIX:-$HOME/.local/share/rfsim/openEMS}"
OPENEMS_SOURCE="${OPENEMS_SOURCE:-$HOME/.cache/rfsim/openEMS-Project}"

configure_homebrew_downloads() {
  # GHCR and raw GitHub occasionally reset HTTP/2 streams on macOS.  Use
  # temporary curl settings for this install only; respect a user's existing
  # settings when they are already present.
  if [[ -z "${CURL_HOME:-}" ]]; then
    RFSIM_CURL_HOME="$(mktemp -d "${TMPDIR:-/tmp}/rfsim-curl-home.XXXXXX")"
    printf '%s\n' '--http1.1' > "$RFSIM_CURL_HOME/.curlrc"
    export CURL_HOME="$RFSIM_CURL_HOME"
  fi
  if [[ -z "${HOMEBREW_CURLRC:-}" ]]; then
    RFSIM_HOMEBREW_CURLRC="$(mktemp "${TMPDIR:-/tmp}/rfsim-curlrc.XXXXXX")"
    printf '%s\n' '--http1.1' > "$RFSIM_HOMEBREW_CURLRC"
    export HOMEBREW_CURLRC="$RFSIM_HOMEBREW_CURLRC"
  fi
  trap 'rm -f "${RFSIM_HOMEBREW_CURLRC:-}"; rm -rf "${RFSIM_CURL_HOME:-}"' EXIT
}

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "RFsim macOS installer must run on macOS." >&2
  exit 2
fi

if [[ ! -x "$KICAD_PYTHON" ]]; then
  echo "KiCad Python was not found at: $KICAD_PYTHON" >&2
  echo "Set KICAD_PYTHON to the Python bundled with your KiCad 10 app." >&2
  exit 2
fi

mkdir -p "$PLUGIN_DIR"
rsync -a --delete \
  --exclude '__pycache__' --exclude '*.pyc' \
  "$ROOT/plugins/" "$PLUGIN_DIR/"
cp "$ROOT/LICENSE" "$PLUGIN_DIR/" 2>/dev/null || true
echo "Installed RFsim $("$KICAD_PYTHON" -c 'import pathlib; p=pathlib.Path("'"$PLUGIN_DIR"'/version.py"); print(next(x.split(chr(34))[1] for x in p.read_text().splitlines() if x.startswith("VERSION")))')"
echo "Plugin directory: $PLUGIN_DIR"

if [[ "${RFSIM_SKIP_PYTHON_DEPS:-0}" != "1" ]]; then
  "$KICAD_PYTHON" -m pip install --user "numpy<2.1" "h5py<3.13" "matplotlib<3.8" scikit-rf
fi

case "${RFSIM_INSTALL_OPENEMS:-none}" in
  none)
    echo
    echo "Solver installation was not changed. For a complete macOS solver:"
    echo "  RFSIM_INSTALL_OPENEMS=source $0"
    echo "Then run: $ROOT/scripts/diagnose_macos.py"
    ;;
  brew)
    command -v brew >/dev/null || { echo "Homebrew is required for brew mode." >&2; exit 2; }
    configure_homebrew_downloads
    echo "Installing the third-party Homebrew openEMS formula."
    echo "The formula currently targets openEMS 0.0.36; inductors and Series RLC require v0.37+."
    brew tap vinn-ie/openems
    brew install openems csxcad
    ;;
  source)
    command -v git >/dev/null || { echo "git is required for source mode." >&2; exit 2; }
    command -v brew >/dev/null || { echo "Homebrew is required for source dependencies." >&2; exit 2; }
    configure_homebrew_downloads
    mkdir -p "$(dirname "$OPENEMS_SOURCE")"
    if [[ ! -d "$OPENEMS_SOURCE/.git" ]]; then
      git clone --recursive https://github.com/thliebig/openEMS-Project.git "$OPENEMS_SOURCE"
    fi
    mkdir -p "$OPENEMS_PREFIX"
    (
      cd "$OPENEMS_SOURCE"
      ./scripts/install_deps.sh --auto --disable-gui --python
      ./update_openEMS.sh "$OPENEMS_PREFIX" --disable-GUI --python
    )
    echo "openEMS source build installed under $OPENEMS_PREFIX"
    ;;
  *)
    echo "RFSIM_INSTALL_OPENEMS must be none, brew, or source." >&2
    exit 2
    ;;
esac

echo
echo "Restart KiCad, open PCB Editor, and enable RFsim from the Action Plugins toolbar."
echo "Use OPENEMS_PATH and RFSIM_PYTHON when your solver is installed elsewhere."
