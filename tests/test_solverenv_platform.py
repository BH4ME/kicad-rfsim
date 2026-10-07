import importlib.util
import os
import stat
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("rfsim_solverenv", ROOT / "plugins" / "solverenv.py")
solverenv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(solverenv)


class SolverEnvironmentTests(unittest.TestCase):
    def test_openems_dirs_expands_user_path_and_discovers_macos_locations(self):
        with tempfile.TemporaryDirectory() as home:
            with mock.patch.dict(os.environ, {"HOME": home, "OPENEMS_PATH": "~/custom-openems"}, clear=False), \
                    mock.patch.object(solverenv, "_platform_prefixes", return_value=("/opt/homebrew/opt", "/usr/local/opt")):
                dirs = solverenv.openems_dirs()
        self.assertEqual(dirs[0], os.path.join(home, "custom-openems"))
        self.assertIn("/opt/homebrew/opt/openems", dirs)
        self.assertIn("/usr/local/opt/openems", dirs)

    def test_solver_python_accepts_macos_python3_venv(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            python = root / "venv" / "bin" / "python3"
            python.parent.mkdir(parents=True)
            python.write_text("#!/bin/sh\n")
            python.chmod(python.stat().st_mode | stat.S_IXUSR)
            with mock.patch.dict(os.environ, {"OPENEMS_PATH": str(root)}, clear=False), \
                    mock.patch.object(solverenv, "_platform_prefixes", return_value=()):
                self.assertEqual(solverenv.solver_python(), str(python))

    def test_runtime_env_adds_macos_library_and_python_paths(self):
        with tempfile.TemporaryDirectory() as root:
            root = Path(root)
            for directory in (root / "lib", root / "bin", root / "python"):
                directory.mkdir()
            with mock.patch.dict(os.environ, {"OPENEMS_PATH": str(root), "PATH": "/usr/bin", "DYLD_LIBRARY_PATH": ""}, clear=False), \
                    mock.patch.object(solverenv, "_platform_prefixes", return_value=()):
                env = solverenv.runtime_env()
        self.assertTrue(env["PATH"].startswith(str(root / "bin") + os.pathsep))
        self.assertTrue(env["DYLD_LIBRARY_PATH"].startswith(str(root / "lib") + os.pathsep))
        self.assertEqual(env["OPENEMS_PATH"], str(root))

    def test_runtime_env_keeps_homebrew_openems_and_csxcad_prefixes_separate(self):
        with tempfile.TemporaryDirectory() as prefix:
            prefix = Path(prefix)
            openems = prefix / "openems"
            csxcad = prefix / "csxcad"
            (openems / "lib").mkdir(parents=True)
            (csxcad / "lib").mkdir(parents=True)
            with mock.patch.dict(os.environ, {"OPENEMS_PATH": "", "CSXCAD_INSTALL_PATH": ""}, clear=False), \
                    mock.patch.object(solverenv, "_platform_prefixes", return_value=(str(prefix),)):
                env = solverenv.runtime_env()
        self.assertEqual(env["OPENEMS_PATH"], str(openems))
        self.assertEqual(env["CSXCAD_INSTALL_PATH"], str(csxcad))
        self.assertIn(str(csxcad / "lib"), env["DYLD_LIBRARY_PATH"])


if __name__ == "__main__":
    unittest.main()
