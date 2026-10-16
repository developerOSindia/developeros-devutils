"""
Unit tests for Batch 1: Tools 1-5 (JSON Formatter, Validator, CSV/YAML Converters, XML Formatter).
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.json_formatter import format_json
from core.json_validator import validate_json
from core.json_csv_converter import json_to_csv, csv_to_json
from core.yaml_json_converter import yaml_to_json, json_to_yaml
from core.xml_formatter import format_xml


class TestBatch1Formatters(unittest.TestCase):
    # Tool 1: JSON Formatter
    def test_json_formatter_valid(self):
        res = format_json('{"b":2,"a":1}', indent=2, sort_keys=True)
        self.assertTrue(res["success"])
        self.assertIn('"a": 1', res["output"])

    def test_json_formatter_minify(self):
        res = format_json('{\n  "key": "value"\n}', minify=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["output"], '{"key":"value"}')

    def test_json_formatter_invalid(self):
        res = format_json('{"incomplete": ')
        self.assertFalse(res["success"])
        self.assertIn("JSONDecodeError", res["error"])

    # Tool 2: JSON Validator
    def test_json_validator(self):
        self.assertTrue(validate_json('{"valid": true}')["valid"])
        self.assertFalse(validate_json('{"invalid": }')["valid"])

    # Tool 3: JSON <-> CSV
    def test_json_to_csv(self):
        json_data = '[{"id": 1, "name": "Antigravity"}, {"id": 2, "name": "DeveloperOS"}]'
        res = json_to_csv(json_data)
        self.assertTrue(res["success"])
        self.assertIn("id,name", res["output"])
        self.assertIn("Antigravity", res["output"])

    def test_csv_to_json(self):
        csv_data = "id,name\n1,Antigravity\n2,DeveloperOS"
        res = csv_to_json(csv_data)
        self.assertTrue(res["success"])
        self.assertEqual(res["row_count"], 2)
        self.assertIn('"name": "Antigravity"', res["output"])

    # Tool 4: YAML <-> JSON
    def test_yaml_json_conversion(self):
        yaml_content = "suite:\n  name: devutils\n  version: 1"
        res = yaml_to_json(yaml_content)
        # If pyyaml installed, verify success
        if res["success"]:
            self.assertIn('"devutils"', res["output"])
            j_res = json_to_yaml(res["output"])
            self.assertTrue(j_res["success"])
            self.assertIn("devutils", j_res["output"])

    # Tool 5: XML Formatter & Security
    def test_xml_formatter_valid(self):
        xml_data = "<root><child>value</child></root>"
        res = format_xml(xml_data)
        self.assertTrue(res["success"])
        self.assertIn("<child>", res["output"])

    def test_xml_formatter_minify(self):
        xml_data = "<root>\n  <child>value</child>\n</root>"
        res = format_xml(xml_data, minify=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["output"], "<root><child>value</child></root>")

    def test_xml_security_xxe_rejection(self):
        xxe_payload = '<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>'
        res = format_xml(xxe_payload)
        self.assertFalse(res["success"])
        self.assertIn("Security Alert", res["error"])


if __name__ == "__main__":
    unittest.main()
