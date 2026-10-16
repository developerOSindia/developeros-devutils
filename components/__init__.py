"""
DeveloperOS Reusable Streamlit UI Components.
Scoped presentation helpers adhering to DeveloperOS design tokens.
"""

from .header import render_header
from .footer import render_footer
from .privacy import render_privacy_badge
from .navigation import render_tool_navigation
from .alerts import render_status_alert
from .related_tools import render_related_tools
from .banner import (
    render_main_promotional_banner,
    render_compact_header_banner,
    render_footer_banner,
    get_main_promotional_banner_html,
    get_compact_header_banner_html,
    get_footer_banner_html,
)

__all__ = [
    "render_header",
    "render_footer",
    "render_privacy_badge",
    "render_tool_navigation",
    "render_status_alert",
    "render_related_tools",
    "render_main_promotional_banner",
    "render_compact_header_banner",
    "render_footer_banner",
    "get_main_promotional_banner_html",
    "get_compact_header_banner_html",
    "get_footer_banner_html",
]
