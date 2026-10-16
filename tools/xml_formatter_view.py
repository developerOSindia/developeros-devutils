"""
XML Formatter & Minifier UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.xml_formatter import format_xml
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_xml_formatter_view():
    st.markdown("### 🗂️ XML Formatter & Minifier")
    st.caption("Prettify, format, or compress XML documents with safe entity-expansion prevention.")
    render_privacy_badge("client_side")

    sample_xml = "<developerOS><suite name=\"devutils\"><tool id=\"1\">XML Formatter</tool></suite></developerOS>"

    col_in, col_out = st.columns([1, 1], gap="medium")
    with col_in:
        st.markdown("**XML Input**")
        raw = st.text_area("XML Input", value=sample_xml, height=260, label_visibility="collapsed")
        c1, c2 = st.columns(2)
        indent = c1.selectbox("Indentation", ["2 spaces", "4 spaces", "Tab"], index=0)
        minify = c2.checkbox("Minify XML", value=False)

    indent_map = {"2 spaces": "  ", "4 spaces": "    ", "Tab": "\t"}

    with col_out:
        st.markdown("**Output**")
        res = format_xml(raw, indent=indent_map[indent], minify=minify)
        if not res["success"]:
            render_status_alert(res["error"], "error")
        else:
            st.code(res["output"], language="xml")
            st.download_button(
                "📥 Download XML",
                data=res["output"],
                file_name="formatted.xml",
                mime="application/xml",
                use_container_width=True
            )
