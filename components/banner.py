"""
DeveloperOS Universal Promotional Banner Component for Streamlit Suites.
Provides three standard variants:
1. Main Promotional Banner (rendered below primary tool interface)
2. Compact Header Banner ("Powered by DeveloperOS ↗")
3. Footer Banner ("Built with ❤️ by DeveloperOS")

Designed with zero external runtime dependencies and safe headless fallback.
"""

from typing import Optional

try:
    import streamlit as st
except ImportError:
    st = None

# Authoritative URLs
MAIN_WEBSITE_URL = "https://developeros.in"
TOOLS_DIRECTORY_URL = "https://toolkit.developeros.in"
GITHUB_ORG_URL = "https://github.com/developerOSindia"
PRIVACY_URL = "https://developeros.in/privacy"

# Standard UTM Query Parameters
UTM_MAIN_PRIMARY = "?utm_source=developeros_tools&utm_medium=main_banner&utm_campaign=ecosystem_referral"
UTM_MAIN_SECONDARY = "?utm_source=developeros_tools&utm_medium=secondary_cta&utm_campaign=tools_directory"
UTM_HEADER = "?utm_source=developeros_tools&utm_medium=header_banner&utm_campaign=powered_by"
UTM_FOOTER = "?utm_source=developeros_tools&utm_medium=footer_link&utm_campaign=ecosystem_referral"

# Official DeveloperOS Isometric Terminal Vector Logo (SVG)
DEVOS_LOGO_SVG = """<svg viewBox="0 0 64 64" width="40" height="40" fill="none" style="flex-shrink: 0;" aria-hidden="true">
  <defs>
    <linearGradient id="promoFavGrad" x1="10%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff3b30"/>
      <stop offset="48%" stop-color="#ff5a3d"/>
      <stop offset="100%" stop-color="#ff914d"/>
    </linearGradient>
    <linearGradient id="promoPanelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1b1b1f"/>
      <stop offset="100%" stop-color="#242428"/>
    </linearGradient>
  </defs>
  <rect x="34" y="12" width="22" height="10" rx="2.5" fill="url(#promoPanelGrad)" stroke="rgba(255,255,255,0.06)"/>
  <rect x="34" y="26" width="22" height="10" rx="2.5" fill="url(#promoPanelGrad)" stroke="rgba(255,255,255,0.06)"/>
  <rect x="34" y="40" width="22" height="10" rx="2.5" fill="url(#promoPanelGrad)" stroke="rgba(255,255,255,0.06)"/>
  <path d="M15 20.5L33.5 14V49.5L15 46Z" fill="#05070a" stroke="url(#promoFavGrad)" stroke-width="2.8" stroke-linejoin="round"/>
  <path d="M15 20.5V46" stroke="url(#promoFavGrad)" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M33.5 14V49.5" stroke="url(#promoFavGrad)" stroke-width="2.8" stroke-linecap="round"/>
  <path d="M22 23L27 25.8L22 28.6" stroke="#f8fafc" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>
  <line x1="23.5" y1="34.2" x2="29.2" y2="34.2" stroke="#f8fafc" stroke-width="2.8" stroke-linecap="round"/>
</svg>"""


def get_main_promotional_banner_html(
    tool_name: Optional[str] = None,
    heading: str = "Enjoying this free tool?",
    description: str = "Discover more developer tools, AI resources, and automation solutions from DeveloperOS.",
    primary_cta_text: str = "Explore DeveloperOS",
    secondary_cta_text: str = "More Free Tools",
    primary_url: Optional[str] = None,
    secondary_url: Optional[str] = None,
) -> str:
    """
    Generates semantic HTML for the Main Promotional Banner.
    Displayed below the primary tool interface.
    """
    p_url = primary_url or f"{MAIN_WEBSITE_URL}{UTM_MAIN_PRIMARY}"
    s_url = secondary_url or f"{TOOLS_DIRECTORY_URL}{UTM_MAIN_SECONDARY}"

    heading_text = f"Enjoying {tool_name}?" if tool_name and heading == "Enjoying this free tool?" else heading

    return f"""
    <section class="devos-promotional-banner" role="region" aria-label="DeveloperOS Promotion" style="
        background: linear-gradient(135deg, rgba(249, 115, 22, 0.08) 0%, rgba(244, 63, 94, 0.04) 50%, rgba(6, 182, 212, 0.06) 100%), #0c0f15;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem 1.75rem;
        margin: 2.5rem 0 1.5rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.25rem;
    ">
        <div style="display: flex; align-items: center; gap: 1.25rem; max-width: 650px;">
            {DEVOS_LOGO_SVG}
            <div>
                <h3 style="margin: 0 0 0.35rem 0; font-size: 1.2rem; font-weight: 700; color: #f8fafc; letter-spacing: -0.01em;">
                    {heading_text}
                </h3>
                <p style="margin: 0; color: #94a3b8; font-size: 0.95rem; line-height: 1.5;">
                    {description}
                </p>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 0.85rem; flex-wrap: wrap;">
            <a href="{p_url}" target="_blank" rel="noopener noreferrer" style="
                background-color: #f97316;
                color: #ffffff;
                font-weight: 600;
                font-size: 0.9rem;
                padding: 0.55rem 1.25rem;
                border-radius: 6px;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                box-shadow: 0 2px 4px rgba(249, 115, 22, 0.25);
                transition: background-color 0.15s ease-in-out;
            ">
                {primary_cta_text} &rarr;
            </a>
            <a href="{s_url}" target="_blank" rel="noopener noreferrer" style="
                background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.15);
                color: #f8fafc;
                font-weight: 600;
                font-size: 0.9rem;
                padding: 0.55rem 1.15rem;
                border-radius: 6px;
                text-decoration: none;
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                transition: background-color 0.15s ease-in-out;
            ">
                {secondary_cta_text}
            </a>
        </div>
    </section>
    """


def get_compact_header_banner_html(
    text: str = "Powered by DeveloperOS ↗",
    url: Optional[str] = None,
) -> str:
    """
    Generates semantic HTML for the Compact Header Banner.
    Display a subtle navigation element in top headers/navbars.
    """
    target_url = url or f"{MAIN_WEBSITE_URL}{UTM_HEADER}"
    return f"""
    <a href="{target_url}" target="_blank" rel="noopener noreferrer" class="devos-compact-header-banner" style="
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background: rgba(249, 115, 22, 0.1);
        border: 1px solid rgba(249, 115, 22, 0.3);
        color: #f97316;
        font-size: 0.78rem;
        font-weight: 600;
        padding: 0.25rem 0.65rem;
        border-radius: 9999px;
        text-decoration: none;
        letter-spacing: 0.01em;
        transition: all 0.15s ease-in-out;
    ">
        <span>⚡</span>
        <span>{text}</span>
    </a>
    """


def get_footer_banner_html() -> str:
    """
    Generates semantic HTML for the Footer Banner.
    Displays:
    "Built with ❤️ by DeveloperOS"
    Links: DeveloperOS website, All tools, GitHub organization, Privacy policy.
    """
    devos_home = f"{MAIN_WEBSITE_URL}{UTM_FOOTER}"
    tools_dir = f"{TOOLS_DIRECTORY_URL}{UTM_FOOTER}"
    privacy_page = f"{PRIVACY_URL}{UTM_FOOTER}"

    return f"""
    <footer class="devos-footer-banner" role="contentinfo" style="
        margin-top: 3.5rem;
        padding: 2rem 0 1.25rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        color: #cbd5e1;
        font-size: 0.875rem;
    ">
        <p style="font-size: 1rem; font-weight: 600; color: #f8fafc; margin: 0 0 0.85rem 0;">
            Built with ❤️ by <a href="{devos_home}" target="_blank" rel="noopener noreferrer" style="color: #f97316; text-decoration: none; font-weight: 700;">DeveloperOS</a>
        </p>
        <div style="display: flex; justify-content: center; align-items: center; gap: 1.25rem; flex-wrap: wrap; margin-bottom: 0.85rem;">
            <a href="{devos_home}" target="_blank" rel="noopener noreferrer" style="color: #67e8f9; text-decoration: none;">
                DeveloperOS Home
            </a>
            <span style="color: rgba(255, 255, 255, 0.2);">•</span>
            <a href="{tools_dir}" target="_blank" rel="noopener noreferrer" style="color: #67e8f9; text-decoration: none;">
                All Tools Directory
            </a>
            <span style="color: rgba(255, 255, 255, 0.2);">•</span>
            <a href="{GITHUB_ORG_URL}" target="_blank" rel="noopener noreferrer" style="color: #67e8f9; text-decoration: none;">
                GitHub Organization
            </a>
            <span style="color: rgba(255, 255, 255, 0.2);">•</span>
            <a href="{privacy_page}" target="_blank" rel="noopener noreferrer" style="color: #67e8f9; text-decoration: none;">
                Privacy Policy
            </a>
        </div>
        <p style="margin: 0.35rem 0; color: #94a3b8; font-size: 0.8rem;">
            DeveloperOS Open-Source Tools Ecosystem • Licensed under the MIT License • Zero Telemetry Guarantee
        </p>
        <p style="margin: 0; color: #6b7c94; font-size: 0.78rem;">
            All processing occurs strictly client-side or in ephemeral in-memory sessions. Zero payload data is persisted.
        </p>
    </footer>
    """


def render_main_promotional_banner(
    tool_name: Optional[str] = None,
    heading: str = "Enjoying this free tool?",
    description: str = "Discover more developer tools, AI resources, and automation solutions from DeveloperOS.",
    primary_cta_text: str = "Explore DeveloperOS",
    secondary_cta_text: str = "More Free Tools",
    primary_url: Optional[str] = None,
    secondary_url: Optional[str] = None,
) -> None:
    """Renders the Main Promotional Banner in Streamlit."""
    if st is not None:
        html = get_main_promotional_banner_html(
            tool_name=tool_name,
            heading=heading,
            description=description,
            primary_cta_text=primary_cta_text,
            secondary_cta_text=secondary_cta_text,
            primary_url=primary_url,
            secondary_url=secondary_url,
        )
        st.markdown(html, unsafe_allow_html=True)


def render_compact_header_banner(
    text: str = "Powered by DeveloperOS ↗",
    url: Optional[str] = None,
) -> None:
    """Renders the Compact Header Banner in Streamlit."""
    if st is not None:
        html = get_compact_header_banner_html(text=text, url=url)
        st.markdown(html, unsafe_allow_html=True)


def render_footer_banner() -> None:
    """Renders the Footer Banner in Streamlit."""
    if st is not None:
        html = get_footer_banner_html()
        st.markdown(html, unsafe_allow_html=True)
