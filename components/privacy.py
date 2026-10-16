"""
DeveloperOS Privacy Badge & Notice Component.
"""

try:
    import streamlit as st
except ImportError:
    st = None


def render_privacy_badge(privacy_model: str = "client_side"):
    """Renders privacy assurance banner."""
    if privacy_model == "client_side":
        badge_text = "Client-Side Processing • Zero Storage Guarantee"
        badge_desc = "Your data stays in your browser session and is never persisted to disk or sent to external servers."
    else:
        badge_text = "Ephemeral In-Memory Processing • Zero Retention"
        badge_desc = "Data is processed strictly in-memory during this execution and immediately discarded."

    html_badge = f"""
    <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.5rem 0.85rem; background-color: #0f172a; border: 1px solid #10b981; border-radius: 0.375rem; margin-bottom: 1.25rem;">
        <span style="color: #10b981; font-size: 1.1rem; line-height: 1;">🛡️</span>
        <div>
            <div style="color: #10b981; font-weight: 600; font-size: 0.82rem; letter-spacing: 0.02em;">
                {badge_text}
            </div>
            <div style="color: #94a3b8; font-size: 0.75rem;">
                {badge_desc}
            </div>
        </div>
    </div>
    """
    st.markdown(html_badge, unsafe_allow_html=True)
