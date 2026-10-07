import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_metadata_advertises_the_mac_release_and_matches_source_version(self):
        metadata = json.loads((ROOT / "metadata.json").read_text())
        source = (ROOT / "plugins" / "version.py").read_text()
        match = re.search(r'^VERSION = "([0-9]+\.[0-9]+\.[0-9]+)"$',
                          source, re.MULTILINE)
        self.assertIsNotNone(match)
        version = match.group(1)
        versions = metadata["versions"]
        self.assertEqual(versions[0]["version"], version)
        self.assertIn("macos", versions[0]["platforms"])


if __name__ == "__main__":
    unittest.main()
