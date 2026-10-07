import stat
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ScriptTests(unittest.TestCase):
    def test_macos_installer_is_executable_and_uses_kicad_plugin_path(self):
        script = ROOT / "scripts" / "install_macos.sh"
        self.assertTrue(script.exists())
        self.assertTrue(script.stat().st_mode & stat.S_IXUSR)
        text = script.read_text()
        self.assertIn("Documents/KiCad/$KICAD_VERSION/scripting/plugins", text)
        self.assertIn("RFSIM_INSTALL_OPENEMS", text)

    def test_diagnostic_script_is_present(self):
        script = ROOT / "scripts" / "diagnose_macos.py"
        self.assertTrue(script.exists())
        self.assertIn("solverenv.runtime_env", script.read_text())

    def test_version_and_package_helpers_are_present(self):
        self.assertIn("choices=(\"patch\", \"minor\", \"major\")",
                      (ROOT / "scripts" / "bump_version.py").read_text())
        self.assertIn("rfsim_v${VERSION}_macos.zip",
                      (ROOT / "scripts" / "package_macos.sh").read_text())


if __name__ == "__main__":
    unittest.main()
