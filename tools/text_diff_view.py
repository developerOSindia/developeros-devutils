"""
Text Diff Checker UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.text_diff import compute_text_diff
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_text_diff_view():
    st.markdown("### 📝 Text Diff Checker")
    st.caption("Compare two code snippets, configuration files, or documents side-by-side with change metrics.")
    render_privacy_badge("client_side")

    sample_orig = """{
  "name": "developeros",
  "version": "1.0.0",
  "tier": "community",
  "theme": "dark"
}"""

    sample_mod = """{
  "name": "developeros",
  "version": "1.1.0",
  "tier": "enterprise",
  "theme": "system",
  "license": "MIT"
}"""

    col_orig, col_mod = st.columns(2)
    with col_orig:
        st.markdown("**Original Text**")
        orig_text = st.text_area("Original", value=sample_orig, height=220, label_visibility="collapsed")
    with col_mod:
        st.markdown("**Modified Text**")
        mod_text = st.text_area("Modified", value=sample_mod, height=220, label_visibility="collapsed")

    context_lines = st.slider("Context Lines around Changes", min_value=0, max_value=10, value=3)

    if orig_text is not None and mod_text is not None:
        diff_res = compute_text_diff(orig_text, mod_text, context_lines=context_lines)
        if diff_res["success"]:
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Similarity", f"{diff_res['similarity_ratio']}%")
            m2.metric("Additions", f"+{diff_res['additions']}")
            m3.metric("Deletions", f"-{diff_res['deletions']}")
            m4.metric("Status", "Differences Found" if diff_res["has_changes"] else "Identical")

            st.markdown("#### Unified Diff Output")
            if diff_res["unified_diff"]:
                st.code(diff_res["unified_diff"], language="diff")
            else:
                render_status_alert("No textual differences detected between Original and Modified.", "info")
        else:
            render_status_alert(diff_res["error"], "error")
