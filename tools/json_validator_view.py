"""
JSON Formatter & Validator UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None
from core.json_validator import validate_and_format_json
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_json_validator_view():
    """Renders the JSON Formatter & Validator tool UI."""
    st.markdown("### 📊 JSON Formatter & Validator")
    st.caption("Inspect, validate, prettify, and minify JSON payloads client-side.")
    render_privacy_badge("client_side")

    col_in, col_out = st.columns([1, 1], gap="medium")

    sample_json = '{"project": "DeveloperOS", "version": "1.0.0", "tools": ["analyzer", "hasher", "validator"], "active": true}'

    with col_in:
        st.markdown("**Raw JSON Input**")
        raw_input = st.text_area(
            "Input JSON",
            value=sample_json,
            height=260,
            label_visibility="collapsed"
        )
        ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)
        indent_val = ctrl_col1.selectbox("Indentation", [2, 4], index=0)
        sort_keys_val = ctrl_col2.checkbox("Sort Keys", value=True)
        minify_val = ctrl_col3.checkbox("Minify", value=False)

    with col_out:
        st.markdown("**Formatted Output & Validation**")
        res = validate_and_format_json(
            raw_input,
            indent=indent_val,
            sort_keys=sort_keys_val,
            minify=minify_val
        )

        if not res["valid"]:
            render_status_alert(res["error"], "error")
            st.info("Ensure all quotes are double quotes (\") and trailing commas are removed.")
        else:
            render_status_alert("Valid JSON syntax!", "success")
            stats = res["stats"]
            st.caption(
                f"Root: `{stats['root_type']}` | Items: `{stats['keys_count']}` | "
                f"Size: `{stats['size_bytes']} B` | Ratio: `{res['compression_ratio']}`"
            )
            st.code(res["formatted"], language="json")

            st.download_button(
                "📥 Download Formatted JSON",
                data=res["formatted"],
                file_name="formatted.json",
                mime="application/json",
                use_container_width=True
            )
