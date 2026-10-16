"""
DeveloperOS Standard Footer Component.
Wraps the Universal Footer Banner ("Built with ❤️ by DeveloperOS").
"""

try:
    import streamlit as st
except ImportError:
    st = None

from components.banner import render_footer_banner, get_footer_banner_html


def render_footer():
    """Renders the standard DeveloperOS footer banner with ecosystem links, privacy guarantee, and MIT notice."""
    render_footer_banner()
