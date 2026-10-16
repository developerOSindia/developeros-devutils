"""
Integration tests for DevUtils Suite 20-tool registration and manifest synchronization.
"""

import sys
import unittest
from pathlib import Path
try:
    import yaml
except ImportError:
    yaml = None

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from tools import registry


def parse_manifest_tool_ids(manifest_text: str) -> list[str]:
    """Extract tool IDs from manifest lines without PyYAML dependency."""
    ids = []
    for line in manifest_text.splitlines():
        line = line.strip()
        if line.startswith("- id:"):
            tool_id = line.split(":", 1)[1].strip().strip('"')
            ids.append(tool_id)
    return ids


class TestSuiteRegistration(unittest.TestCase):
    def test_all_20_tools_registered(self):
        all_tools = registry.list_all()
        self.assertEqual(len(all_tools), 20, f"Expected exactly 20 tools, found {len(all_tools)}")

    def test_categories(self):
        categories = registry.get_categories()
        expected_cats = {
            "Formatters & Converters",
            "Security & Encoders",
            "Text & Inspection",
            "Web & Design Tools"
        }
        self.assertEqual(set(categories), expected_cats)

    def test_manifest_matches_registry(self):
        manifest_path = SUITE_ROOT / "manifest.yaml"
        self.assertTrue(manifest_path.exists())
        content = manifest_path.read_text(encoding="utf-8")

        if yaml is not None:
            manifest_data = yaml.safe_load(content)
            manifest_tool_ids = [t["id"] for t in manifest_data["tools"]]
        else:
            manifest_tool_ids = parse_manifest_tool_ids(content)

        registered_tool_ids = [t.id for t in registry.list_all()]

        self.assertEqual(len(manifest_tool_ids), 20)
        self.assertEqual(set(manifest_tool_ids), set(registered_tool_ids))

    def test_each_tool_contract(self):
        for tool in registry.list_all():
            self.assertTrue(tool.id.startswith("tool-"), f"Tool ID {tool.id} invalid")
            self.assertTrue(callable(tool.ui_entrypoint), f"Tool {tool.id} UI entrypoint is not callable")
            self.assertTrue(tool.name, f"Tool {tool.id} missing name")
            self.assertTrue(tool.description, f"Tool {tool.id} missing description")
            self.assertEqual(tool.privacy_classification, "client_side")


if __name__ == "__main__":
    unittest.main()
