"""
Unit tests for Batch 4: Tools 16-20 (HTML Minifier, CSS Minifier, Color Converter, Text Case Converter, QR Code Generator).
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.html_minifier import minify_html
from core.css_minifier import minify_css
from core.color_converter import convert_color, hex_to_rgb, rgb_to_hex
from core.text_case_converter import convert_cases
from core.qr_code_generator import generate_qr_code


class TestBatch4WebDesign(unittest.TestCase):
    # Tool 16: HTML Minifier
    def test_html_minifier_basic(self):
        raw = "<div> \n  <p>Hello   World</p> \n<!-- Comment -->\n</div>"
        res = minify_html(raw)
        self.assertTrue(res["success"])
        self.assertNotIn("<!-- Comment -->", res["output"])
        self.assertIn("<div><p>Hello World</p></div>", res["output"])
        self.assertGreater(res["savings_percent"], 0.0)

    def test_html_minifier_preserves_code_and_pre(self):
        raw = "<pre>   preserve\n   exact   spaces   </pre>"
        res = minify_html(raw)
        self.assertTrue(res["success"])
        self.assertIn("   preserve\n   exact   spaces   ", res["output"])

    # Tool 17: CSS Minifier
    def test_css_minifier_basic(self):
        raw = """
        /* Header style */
        .header {
            color: #ffffff;
            margin: 10px 20px;
        }
        """
        res = minify_css(raw)
        self.assertTrue(res["success"])
        self.assertNotIn("/* Header style */", res["output"])
        self.assertEqual(res["output"], ".header{color:#ffffff;margin:10px 20px}")
        self.assertGreater(res["savings_percent"], 0.0)

    # Tool 18: Color Converter
    def test_color_converter_hex(self):
        res = convert_color("#6366f1")
        self.assertTrue(res["success"])
        self.assertEqual(res["hex"], "#6366f1")
        self.assertEqual(res["rgb_tuple"], (99, 102, 241))
        self.assertIn("hsl", res)
        self.assertIn("cmyk", res)
        self.assertGreater(res["contrast_on_black"], 1.0)
        self.assertGreater(res["contrast_on_white"], 1.0)

    def test_color_converter_invalid(self):
        res = convert_color("not-a-color-xyz")
        self.assertFalse(res["success"])
        self.assertIn("Color Parsing Error", res["error"])

    # Tool 19: Text Case Converter
    def test_text_case_converter(self):
        res = convert_cases("developerOS tools ecosystem")
        self.assertTrue(res["success"])
        self.assertEqual(res["camel_case"], "developerOsToolsEcosystem")
        self.assertEqual(res["pascal_case"], "DeveloperOsToolsEcosystem")
        self.assertEqual(res["snake_case"], "developer_os_tools_ecosystem")
        self.assertEqual(res["constant_case"], "DEVELOPER_OS_TOOLS_ECOSYSTEM")
        self.assertEqual(res["kebab_case"], "developer-os-tools-ecosystem")
        self.assertEqual(res["cobol_case"], "DEVELOPER-OS-TOOLS-ECOSYSTEM")

    # Tool 20: QR Code Generator
    def test_qr_code_generator_success(self):
        res = generate_qr_code("https://developeros.in")
        self.assertTrue(res["success"])
        self.assertIsNotNone(res["svg_content"])
        self.assertEqual(res["payload_length"], 22)

    def test_qr_code_generator_limits(self):
        huge_payload = "A" * 5000
        res = generate_qr_code(huge_payload)
        self.assertFalse(res["success"])
        self.assertIn("exceeds QR code limit", res["error"])


if __name__ == "__main__":
    unittest.main()
