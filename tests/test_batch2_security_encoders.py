"""
Unit tests for Batch 2: Tools 6-10 (Base64 Codec, JWT Decoder, UUID Generator, Regex Tester, Cron Builder).
"""

import sys
import unittest
from pathlib import Path

SUITE_ROOT = Path(__file__).resolve().parent.parent
if str(SUITE_ROOT) not in sys.path:
    sys.path.insert(0, str(SUITE_ROOT))

from core.base64_codec import encode_base64, decode_base64
from core.jwt_decoder import decode_jwt, SECURITY_DISCLAIMER
from core.uuid_generator import generate_uuids
from core.regex_tester import test_regex
from core.cron_builder import build_cron, explain_cron, PRESETS


class TestBatch2SecurityEncoders(unittest.TestCase):
    # Tool 6: Base64 Encoder/Decoder
    def test_base64_roundtrip_standard(self):
        original = "DeveloperOS Tools Ecosystem 🚀"
        enc = encode_base64(original, url_safe=False)
        self.assertTrue(enc["success"])
        dec = decode_base64(enc["output"], url_safe=False)
        self.assertTrue(dec["success"])
        self.assertEqual(dec["output"], original)

    def test_base64_url_safe(self):
        text = "https://developeros.in/tools?query=test&flag=1"
        enc = encode_base64(text, url_safe=True)
        self.assertTrue(enc["success"])
        self.assertNotIn("+", enc["output"])
        self.assertNotIn("/", enc["output"])
        dec = decode_base64(enc["output"], url_safe=True)
        self.assertTrue(dec["success"])
        self.assertEqual(dec["output"], text)

    def test_base64_invalid_decode(self):
        res = decode_base64("!!!InvalidBase64@@@")
        self.assertFalse(res["success"])

    # Tool 7: JWT Decoder
    def test_jwt_decoder_valid(self):
        # Sample standard token with sub and exp
        # Header: {"alg":"HS256","typ":"JWT"} -> eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
        # Payload: {"sub":"1234567890","name":"DeveloperOS User","iat":1516239022} -> eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRldmVsb3Blck9TIFVzZXIiLCJpYXQiOjE1MTYyMzkwMjJ9
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRldmVsb3Blck9TIFVzZXIiLCJpYXQiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        res = decode_jwt(token)
        self.assertTrue(res["success"])
        self.assertEqual(res["header"]["alg"], "HS256")
        self.assertEqual(res["payload"]["name"], "DeveloperOS User")
        self.assertIn("iat_formatted", res["claims_info"])
        self.assertIn("SECURITY NOTICE", res["security_disclaimer"])

    def test_jwt_decoder_invalid_parts(self):
        res = decode_jwt("invalid.token")
        self.assertFalse(res["success"])
        self.assertIn("Expected 3 period-separated parts", res["error"])

    # Tool 8: UUID Generator
    def test_uuid_generator_v4(self):
        res = generate_uuids(count=5, version=4, uppercase=True, hyphens=True, braces=False)
        self.assertTrue(res["success"])
        self.assertEqual(len(res["uuids"]), 5)
        for u in res["uuids"]:
            self.assertEqual(len(u), 36)
            self.assertEqual(u, u.upper())
            self.assertIn("-", u)

    def test_uuid_generator_formatting_options(self):
        res = generate_uuids(count=2, version=4, uppercase=False, hyphens=False, braces=True)
        self.assertTrue(res["success"])
        for u in res["uuids"]:
            self.assertTrue(u.startswith("{") and u.endswith("}"))
            self.assertNotIn("-", u)
            self.assertEqual(len(u), 34)  # 32 chars + 2 braces

    # Tool 9: Regex Tester
    def test_regex_tester_matches(self):
        text = "Errors: 404 Not Found, 500 Internal Error, 200 OK"
        pattern = r"\b(?P<code>\d{3})\b"
        res = test_regex(pattern, text)
        self.assertTrue(res["success"])
        self.assertEqual(res["match_count"], 3)
        self.assertEqual(res["matches"][0]["groupdict"], {"code": "404"})

    def test_regex_tester_substitution(self):
        text = "Contact us at contact@developeros.in or support@developeros.in"
        pattern = r"[\w\.-]+@[\w\.-]+"
        res = test_regex(pattern, text, replacement="[REDACTED]")
        self.assertTrue(res["success"])
        self.assertEqual(res["replaced_output"], "Contact us at [REDACTED] or [REDACTED]")

    def test_regex_tester_invalid_syntax(self):
        res = test_regex("[unclosed group", "sample text")
        self.assertFalse(res["success"])
        self.assertIn("Regex Syntax Error", res["error"])

    # Tool 10: Cron Builder & Explainer
    def test_cron_builder(self):
        expr = build_cron("0", "12", "*", "*", "1-5")
        self.assertEqual(expr, "0 12 * * 1-5")

    def test_cron_explainer_valid(self):
        expr = "*/15 0 * * 0"
        res = explain_cron(expr)
        self.assertTrue(res["success"])
        self.assertIn("every 15 minutes", res["description"])
        self.assertIn("Sunday", res["description"])

    def test_cron_explainer_invalid(self):
        res = explain_cron("0 * * *")  # only 4 parts
        self.assertFalse(res["success"])
        self.assertIn("Expected 5 fields", res["error"])


if __name__ == "__main__":
    unittest.main()
