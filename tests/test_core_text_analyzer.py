"""
Unit tests for core.text_analyzer module.
"""

import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.text_analyzer import calculate_entropy, analyze_text, transform_text_case


class TestTextAnalyzerCore(unittest.TestCase):
    def test_calculate_entropy(self):
        self.assertEqual(calculate_entropy(""), 0.0)
        # All same characters -> 0 bits of surprise
        self.assertEqual(calculate_entropy("aaaaaa"), 0.0)
        # Highly random characters -> higher entropy
        self.assertGreater(calculate_entropy("abcdefghijklmnopqrstuvwxyz1234567890"), 4.0)

    def test_analyze_text_metrics(self):
        sample = "The quick brown fox jumps over the lazy dog."
        metrics = analyze_text(sample)
        self.assertTrue(metrics.success)
        self.assertEqual(metrics.total_words, 9)
        self.assertEqual(metrics.total_lines, 1)
        self.assertGreater(metrics.reading_time_sec, 0)
        self.assertGreater(metrics.shannon_entropy, 3.0)

    def test_analyze_empty_text(self):
        metrics = analyze_text("")
        self.assertTrue(metrics.success)
        self.assertEqual(metrics.total_words, 0)
        self.assertEqual(metrics.total_chars, 0)

    def test_case_transformations(self):
        text = "developer os open source"
        self.assertEqual(transform_text_case(text, "upper")["output"], "DEVELOPER OS OPEN SOURCE")
        self.assertEqual(transform_text_case(text, "lower")["output"], "developer os open source")
        self.assertEqual(transform_text_case(text, "title")["output"], "Developer Os Open Source")
        self.assertEqual(transform_text_case(text, "snake")["output"], "developer_os_open_source")
        self.assertEqual(transform_text_case(text, "kebab")["output"], "developer-os-open-source")
        self.assertEqual(transform_text_case(text, "camel")["output"], "developerOsOpenSource")


if __name__ == "__main__":
    unittest.main()
