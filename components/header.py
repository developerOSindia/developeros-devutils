"""
DeveloperOS Standard Header Component.
Includes brand identification, suite breadcrumb, and the Compact Header Banner ("Powered by DeveloperOS ↗").
"""

try:
    import streamlit as st
except ImportError:
    st = None

from components.banner import DEVOS_LOGO_SVG, get_compact_header_banner_html


def render_header(
    suite_title: str = "DeveloperOS Tools Suite",
    category_badge: str = "Utilities",
    github_repo: str = "https://github.com/developerOSindia"
):
    """Renders the standard DeveloperOS branded header with Compact Header Banner."""
    compact_banner = get_compact_header_banner_html()

    html_header = f"""
    <header class="devos-app-header" role="banner" style="display: flex; justify-content: space-between; align-items: center; padding: 0.75rem 1.25rem; margin-bottom: 1.5rem; background-color: #0c0f15; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 0.75rem; flex-wrap: wrap; gap: 0.75rem;">
        <div style="display: flex; align-items: center; gap: 0.85rem;">
            {DEVOS_LOGO_SVG}
            <div>
                <a href="https://developeros.in" target="_blank" rel="noopener noreferrer" style="font-weight: 700; color: #f8fafc; text-decoration: none; font-size: 1.15rem; letter-spacing: -0.02em;">DeveloperOS</a>
                <span style="color: #6b7c94; margin: 0 0.35rem;">/</span>
                <span style="color: #cbd5e1; font-size: 0.95rem; font-weight: 500;">{suite_title}</span>
            </div>
            <span style="background-color: #08090c; color: #67e8f9; border: 1px solid rgba(6, 182, 212, 0.3); font-size: 0.75rem; font-weight: 600; padding: 0.15rem 0.55rem; border-radius: 9999px;">
                {category_badge}
            </span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap;">
            {compact_banner}
            <a href="https://tools.developeros.in" target="_blank" rel="noopener noreferrer" style="color: #94a3b8; text-decoration: none; font-size: 0.85rem; padding: 0.28rem 0.65rem; border-radius: 0.375rem; border: 1px solid rgba(255, 255, 255, 0.1); transition: border-color 0.15s;">
                Tools Directory
            </a>
            <a href="{github_repo}" target="_blank" rel="noopener noreferrer" style="background-color: #f97316; color: #ffffff; text-decoration: none; font-size: 0.85rem; font-weight: 600; padding: 0.28rem 0.85rem; border-radius: 0.375rem; transition: background-color 0.15s;">
                GitHub
            </a>
        </div>
    </header>
    """
    if st is not None:
        st.markdown(html_header, unsafe_allow_html=True)
