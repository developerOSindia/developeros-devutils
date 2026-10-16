"""
CSS Minifier UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.css_minifier import minify_css
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_css_minifier_view():
    st.markdown("### 🎨 CSS Minifier")
    st.caption("Strip comments, normalize selectors, collapse whitespace, and minimize CSS assets.")
    render_privacy_badge("client_side")

    sample_css = """/* DeveloperOS Theme Rules */
:root {
    --devos-primary: #6366f1;
    --devos-background: #0f172a;
    --devos-text: #f8fafc;
}

.developer-card {
    background-color: var(--devos-background);
    color: var(--devos-text);
    padding: 16px 24px;
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.developer-card:hover {
    border-color: var(--devos-primary);
    transform: translateY(-2px);
}
"""

    strip_comments = st.checkbox("Strip CSS Comments (/* ... */)", value=True)

    col_in, col_out = st.columns(2, gap="medium")
    with col_in:
        st.markdown("**Original CSS Stylesheet**")
        raw_css = st.text_area("CSS Input", value=sample_css, height=300, label_visibility="collapsed")

    with col_out:
        st.markdown("**Minified Output**")
        if raw_css:
            res = minify_css(raw_css, remove_comments=strip_comments)
            if res["success"]:
                st.text_area("Minified CSS", value=res["output"], height=300, label_visibility="collapsed")
                st.download_button(
                    label="📥 Download Minified CSS",
                    data=res["output"],
                    file_name="styles.min.css",
                    mime="text/css"
                )
            else:
                render_status_alert(res["error"], "error")

    if raw_css and res.get("success"):
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Original Size", f"{res['original_bytes']} B")
        m2.metric("Minified Size", f"{res['minified_bytes']} B")
        m3.metric("Bytes Saved", f"{res['saved_bytes']} B")
        m4.metric("Compression Ratio", f"{res['savings_percent']}%")
