"""
Unit Tests for DeveloperOS Universal Promotional Banner Streamlit Components.
Tests HTML rendering, destination URLs, UTM parameters, and accessibility attributes.
"""

import unittest
from pathlib import Path

# Add template root to sys.path
TEMPLATE_ROOT = Path(__file__).resolve().parent.parent

from components.banner import (
    MAIN_WEBSITE_URL,
    TOOLS_DIRECTORY_URL,
    GITHUB_ORG_URL,
    PRIVACY_URL,
    get_main_promotional_banner_html,
    get_compact_header_banner_html,
    get_footer_banner_html,
)


class TestBannerComponents(unittest.TestCase):
    def test_main_promotional_banner_default(self):
        """Verifies default Main Promotional Banner HTML rendering."""
        html = get_main_promotional_banner_html()
        self.assertIn("Enjoying this free tool?", html)
        self.assertIn("Discover more developer tools, AI resources, and automation solutions from DeveloperOS.", html)
        self.assertIn("Explore DeveloperOS &rarr;", html)
        self.assertIn("More Free Tools", html)
        self.assertIn(MAIN_WEBSITE_URL, html)
        self.assertIn(TOOLS_DIRECTORY_URL, html)
        self.assertIn('target="_blank"', html)
        self.assertIn('rel="noopener noreferrer"', html)
        self.assertIn('role="region"', html)
        self.assertIn('aria-label="DeveloperOS Promotion"', html)

    def test_main_promotional_banner_custom_tool(self):
        """Verifies Main Promotional Banner with tool-specific heading."""
        html = get_main_promotional_banner_html(tool_name="JSON Validator")
        self.assertIn("Enjoying JSON Validator?", html)

    def test_main_promotional_banner_custom_urls(self):
        """Verifies custom URLs and CTA text overrides."""
        custom_p = "https://developeros.in/custom-explore"
        custom_s = "https://tools.developeros.in/custom-tools"
        html = get_main_promotional_banner_html(
            heading="Custom Heading",
            primary_cta_text="Start Now",
            secondary_cta_text="Browse All",
            primary_url=custom_p,
            secondary_url=custom_s,
        )
        self.assertIn("Custom Heading", html)
        self.assertIn("Start Now &rarr;", html)
        self.assertIn("Browse All", html)
        self.assertIn(custom_p, html)
        self.assertIn(custom_s, html)

    def test_compact_header_banner(self):
        """Verifies Compact Header Banner ('Powered by DeveloperOS ↗')."""
        html = get_compact_header_banner_html()
        self.assertIn("Powered by DeveloperOS ↗", html)
        self.assertIn(MAIN_WEBSITE_URL, html)
        self.assertIn("utm_medium=header_banner", html)
        self.assertIn('target="_blank"', html)
        self.assertIn('rel="noopener noreferrer"', html)

    def test_footer_banner(self):
        """Verifies Universal Footer Banner ('Built with ❤️ by DeveloperOS')."""
        html = get_footer_banner_html()
        self.assertIn("Built with ❤️ by", html)
        self.assertIn(MAIN_WEBSITE_URL, html)
        self.assertIn(TOOLS_DIRECTORY_URL, html)
        self.assertIn(GITHUB_ORG_URL, html)
        self.assertIn(PRIVACY_URL, html)
        self.assertIn('role="contentinfo"', html)
        self.assertIn("Zero Telemetry Guarantee", html)
        self.assertIn('target="_blank"', html)
        self.assertIn('rel="noopener noreferrer"', html)


if __name__ == "__main__":
    unittest.main()
