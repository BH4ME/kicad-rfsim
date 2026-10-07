#!/usr/bin/env python3
"""Print and validate the macOS RFsim runtime discovered by the plugin."""

import importlib.util
import json
import os
import platform
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("rfsim_solverenv", ROOT / "plugins" / "solverenv.py")
solverenv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solverenv)


def main():
    print("RFsim macOS diagnostic")
    print("platform:", platform.platform())
    print("architecture:", platform.machine())
    print("python:", sys.executable)
    print("openEMS search paths:")
    for path in solverenv.openems_dirs():
        print("  ", path, "[present]" if os.path.isdir(path) else "[missing]")
    solver = solverenv.solver_python()
    if not solver:
        print("solver Python: not found")
        print("Set RFSIM_PYTHON or install openEMS under ~/openEMS.")
        return 1
    print("solver Python:", solver)
    code = (
        "import importlib, json\n"
        "out = {}\n"
        "for name in ('numpy', 'h5py', 'CSXCAD', 'openEMS'):\n"
        "  try:\n"
        "    module = importlib.import_module(name)\n"
        "    out[name] = {'ok': True, 'file': getattr(module, '__file__', None)}\n"
        "  except Exception as exc:\n"
        "    out[name] = {'ok': False, 'error': '%s: %s' % (type(exc).__name__, exc)}\n"
        "try:\n"
        "  from CSXCAD import CSProperties\n"
        "  out['series_rlc_api'] = {'ok': hasattr(CSProperties.CSPropLumpedElement, 'SetLEtype')}\n"
        "except Exception as exc:\n"
        "  out['series_rlc_api'] = {'ok': False, 'error': '%s: %s' % (type(exc).__name__, exc)}\n"
        "print(json.dumps(out))\n"
    )
    result = subprocess.run([solver, "-c", code], env=solverenv.runtime_env(),
                            text=True, capture_output=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.returncode:
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)
        return result.returncode
    data = json.loads(result.stdout.strip().splitlines()[-1])
    failed = [name for name, info in data.items() if not info["ok"]]
    if failed:
        print("failed modules:", ", ".join(failed))
        if "series_rlc_api" in failed:
            print("openEMS must be v0.37+ for inductor and Series RLC support.")
        return 1
    print("All solver modules imported successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
