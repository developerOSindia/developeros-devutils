"""
JSON Formatter UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.json_formatter import format_json
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_json_formatter_view():
    st.markdown("### 🛠️ JSON Formatter & Minifier")
    st.caption("Prettify, format, or compress JSON documents client-side.")
    render_privacy_badge("client_side")

    sample_json = '{"name":"DeveloperOS","suite":"devutils","tools_count":20,"features":["offline","zero-storage"]}'

    col_in, col_out = st.columns([1, 1], gap="medium")
    with col_in:
        st.markdown("**Input JSON**")
        raw_text = st.text_area("JSON Input", value=sample_json, height=260, label_visibility="collapsed")
        c1, c2, c3 = st.columns(3)
        indent = c1.selectbox("Indent", [2, 4], index=0, key="jf_indent")
        sort_keys = c2.checkbox("Sort Keys", value=False, key="jf_sort")
        minify = c3.checkbox("Minify", value=False, key="jf_mini")

    with col_out:
        st.markdown("**Output**")
        res = format_json(raw_text, indent=indent, sort_keys=sort_keys, minify=minify)
        if not res["success"]:
            render_status_alert(res["error"], "error")
        else:
            st.code(res["output"], language="json")
            if res.get("stats"):
                s = res["stats"]
                st.caption(f"Original: {s['original_size']} B | Result: {s['formatted_size']} B | Items: {s['items_count']}")
            st.download_button(
                "📥 Download JSON",
                data=res["output"],
                file_name="formatted.json",
                mime="application/json",
                use_container_width=True
            )
