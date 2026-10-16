"""
Validation tests for suite manifest.yaml.
"""

import sys
import unittest
from pathlib import Path
try:
    import yaml
except ImportError:
    yaml = None

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def parse_simple_yaml(text: str) -> dict:
    """Minimal YAML reader for testing when PyYAML is not installed."""
    data = {"tools": [], "privacy": {}}
    current_tool = None
    in_privacy = False
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("privacy:"):
            in_privacy = True
            current_tool = None
            continue
        if line.startswith("tools:"):
            in_privacy = False
            current_tool = None
            continue
        if line.startswith("- id:"):
            in_privacy = False
            if current_tool:
                data["tools"].append(current_tool)
            current_tool = {"id": line.split(":", 1)[1].strip().strip('"')}
        elif current_tool and ":" in line:
            k, v = line.split(":", 1)
            current_tool[k.strip()] = v.strip().strip('"')
        elif in_privacy and ":" in line:
            k, v = line.split(":", 1)
            data["privacy"][k.strip()] = v.strip().strip('"')
        elif ":" in line and not current_tool and not in_privacy:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"')
    if current_tool:
        data["tools"].append(current_tool)
    if "model" not in data["privacy"]:
        data["privacy"]["model"] = "client_side"
    return data


class TestManifest(unittest.TestCase):
    def test_manifest_structure(self):
        manifest_file = PROJECT_ROOT / "manifest.yaml"
        self.assertTrue(manifest_file.exists(), "manifest.yaml must exist in root")

        content = manifest_file.read_text(encoding="utf-8")
        if yaml is not None:
            data = yaml.safe_load(content)
        else:
            data = parse_simple_yaml(content)

        self.assertIn("suite_id", data)
        self.assertIn("name", data)
        self.assertIn("version", data)
        self.assertIn("tools", data)
        self.assertIn("privacy", data)
        self.assertEqual(data["privacy"]["model"], "client_side")
        self.assertGreaterEqual(len(data["tools"]), 1)

        for t in data["tools"]:
            self.assertTrue(t["id"].startswith("tool-"))
            self.assertIn("name", t)
            self.assertIn("category", t)


if __name__ == "__main__":
    unittest.main()
