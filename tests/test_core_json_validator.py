"""
Unit tests for core.json_validator module.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.json_validator import validate_and_format_json


class TestJsonValidatorCore(unittest.TestCase):
    def test_valid_json(self):
        sample = '{"b": 2, "a": 1}'
        res = validate_and_format_json(sample, indent=2, sort_keys=True)
        self.assertTrue(res["valid"])
        self.assertIn('"a": 1', res["formatted"])
        self.assertEqual(res["stats"]["root_type"], "dict")
        self.assertEqual(res["stats"]["keys_count"], 2)

    def test_minify_json(self):
        sample = '{\n  "name": "DeveloperOS"\n}'
        res = validate_and_format_json(sample, minify=True)
        self.assertTrue(res["valid"])
        self.assertEqual(res["formatted"], '{"name":"DeveloperOS"}')

    def test_invalid_json(self):
        sample = '{"name": "DeveloperOS",}'  # trailing comma
        res = validate_and_format_json(sample)
        self.assertFalse(res["valid"])
        self.assertIn("JSONDecodeError", res["error"])
        self.assertGreater(res["line"], 0)


if __name__ == "__main__":
    unittest.main()
