"""
Unit tests for Batch 3: Tools 11-15 (Unix Timestamp, URL Codec, Text Diff, Hash Calculator, Markdown Previewer).
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.unix_timestamp import timestamp_to_datetimes, datetime_to_timestamp, get_current_timestamp
from core.url_codec import encode_url, decode_url, parse_url_components
from core.text_diff import compute_text_diff
from core.hash_calculator import generate_hashes, generate_hmac, verify_hash
from core.markdown_previewer import analyze_markdown


class TestBatch3TextInspection(unittest.TestCase):
    # Tool 11: Unix Timestamp Converter
    def test_timestamp_to_datetimes_valid(self):
        # 1700000000 is 2023-11-14 22:13:20 UTC
        res = timestamp_to_datetimes(1700000000)
        self.assertTrue(res["success"])
        self.assertEqual(res["seconds"], 1700000000)
        self.assertEqual(res["milliseconds"], 1700000000000)
        self.assertIn("2023-11-14", res["iso_8601"])

    def test_timestamp_millis_detection(self):
        res = timestamp_to_datetimes(1700000000000, is_millis=True)
        self.assertTrue(res["success"])
        self.assertEqual(res["seconds"], 1700000000)

    def test_datetime_to_timestamp_valid(self):
        res = datetime_to_timestamp("2023-11-14 22:13:20")
        self.assertTrue(res["success"])
        self.assertEqual(res["seconds"], 1700000000)

    def test_current_timestamp(self):
        curr = get_current_timestamp()
        self.assertGreater(curr["seconds"], 1700000000)

    # Tool 12: URL Codec & Parser
    def test_url_encode_decode(self):
        raw = "DeveloperOS Tools & Utilities=100%"
        enc = encode_url(raw, plus_spaces=True)
        self.assertTrue(enc["success"])
        self.assertIn("+", enc["output"])

        dec = decode_url(enc["output"], plus_spaces=True)
        self.assertTrue(dec["success"])
        self.assertEqual(dec["output"], raw)

    def test_url_parse_components(self):
        url = "https://developeros.in:8080/tools?category=security&page=1#top"
        parsed = parse_url_components(url)
        self.assertTrue(parsed["success"])
        self.assertEqual(parsed["scheme"], "https")
        self.assertEqual(parsed["hostname"], "developeros.in")
        self.assertEqual(parsed["port"], 8080)
        self.assertEqual(parsed["path"], "/tools")
        self.assertEqual(parsed["fragment"], "top")
        self.assertEqual(parsed["query_params"]["category"], ["security"])

    # Tool 13: Text Diff Checker
    def test_text_diff_has_changes(self):
        orig = "line 1\nline 2\nline 3\n"
        mod = "line 1\nline 2 modified\nline 3\nline 4\n"
        diff = compute_text_diff(orig, mod)
        self.assertTrue(diff["success"])
        self.assertTrue(diff["has_changes"])
        self.assertGreater(diff["additions"], 0)
        self.assertGreater(diff["deletions"], 0)
        self.assertIn("--- Original", diff["unified_diff"])
        self.assertIn("+++ Modified", diff["unified_diff"])

    def test_text_diff_identical(self):
        text = "identical content\nsecond line"
        diff = compute_text_diff(text, text)
        self.assertTrue(diff["success"])
        self.assertFalse(diff["has_changes"])
        self.assertEqual(diff["similarity_ratio"], 100.0)

    # Tool 14: Hash Calculator
    def test_hash_calculator_generation(self):
        text = "antigravity"
        res = generate_hashes(text)
        self.assertTrue(res["success"])
        # Known SHA256 of "antigravity"
        self.assertIn("SHA256", res["hashes"])
        self.assertIn("MD5", res["hashes"])
        self.assertEqual(len(res["hashes"]["SHA256"]), 64)

    def test_hmac_and_verify(self):
        message = "payload-data"
        secret = "secret-key"
        res = generate_hmac(message, secret, algorithm="sha256")
        self.assertTrue(res["success"])
        self.assertTrue(verify_hash(res["hmac"], res["hmac"]))
        self.assertFalse(verify_hash(res["hmac"], "wrong-hash"))

    # Tool 15: Markdown Previewer
    def test_markdown_analyzer(self):
        md = "# Heading 1\n\nSome text with a [link](https://developeros.in).\n\n## Subheading\n\n![Logo](logo.png)\n\n```python\nprint(1)\n```\n"
        res = analyze_markdown(md)
        self.assertTrue(res["success"])
        self.assertEqual(res["headings_count"], 2)
        self.assertEqual(res["links_count"], 1)
        self.assertEqual(res["images_count"], 1)
        self.assertEqual(res["code_blocks_count"], 1)
        self.assertFalse(res["has_unsafe_html"])

    def test_markdown_unsafe_html_detection(self):
        md = "# Title\n<script>alert(1)</script>"
        res = analyze_markdown(md)
        self.assertTrue(res["success"])
        self.assertTrue(res["has_unsafe_html"])
        self.assertIn("script", res["unsafe_tags_found"])


if __name__ == "__main__":
    unittest.main()
