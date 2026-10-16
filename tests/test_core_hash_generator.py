"""
Unit tests for core.hash_generator module.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.hash_generator import generate_hashes, generate_hmac, verify_hash


class TestHashGeneratorCore(unittest.TestCase):
    def test_generate_hashes(self):
        res = generate_hashes("DeveloperOS")
        self.assertTrue(res["success"])
        hashes = res["hashes"]
        self.assertIn("SHA256", hashes)
        self.assertIn("MD5", hashes)
        self.assertIn("SHA512", hashes)
        self.assertEqual(len(hashes["SHA256"]), 64)
        self.assertEqual(len(hashes["MD5"]), 32)

    def test_generate_hmac(self):
        res = generate_hmac("message", "secret-key", "sha256")
        self.assertTrue(res["success"])
        self.assertEqual(len(res["hmac"]), 64)

    def test_verify_hash(self):
        res = generate_hashes("DeveloperOS")
        sha256_hash = res["hashes"]["SHA256"]
        self.assertTrue(verify_hash(sha256_hash, sha256_hash))
        self.assertTrue(verify_hash(sha256_hash.upper(), sha256_hash.lower()))
        self.assertFalse(verify_hash("wronghash", sha256_hash))


if __name__ == "__main__":
    unittest.main()
