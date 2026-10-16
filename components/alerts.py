"""
DeveloperOS Standard Alert & Status Notification Component.
"""

try:
    import streamlit as st
except ImportError:
    st = None


def render_status_alert(message: str, status_type: str = "info"):
    """Renders accessible status alerts using standard theme tokens."""
    color_map = {
        "success": {"bg": "rgba(16, 185, 129, 0.12)", "border": "#10b981", "icon": "✅", "text": "#34d399"},
        "warning": {"bg": "rgba(245, 158, 11, 0.12)", "border": "#f59e0b", "icon": "⚠️", "text": "#fbbf24"},
        "error": {"bg": "rgba(239, 68, 68, 0.12)", "border": "#ef4444", "icon": "❌", "text": "#f87171"},
        "info": {"bg": "rgba(37, 99, 235, 0.12)", "border": "#2563eb", "icon": "ℹ️", "text": "#60a5fa"},
    }
    cfg = color_map.get(status_type, color_map["info"])

    html_alert = f"""
    <div style="display: flex; align-items: center; gap: 0.6rem; padding: 0.65rem 0.85rem; background-color: {cfg['bg']}; border: 1px solid {cfg['border']}; border-radius: 0.375rem; margin: 0.75rem 0;">
        <span>{cfg['icon']}</span>
        <span style="color: {cfg['text']}; font-size: 0.85rem; font-weight: 500;">
            {message}
        </span>
    </div>
    """
    st.markdown(html_alert, unsafe_allow_html=True)
