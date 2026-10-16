"""
JSON <-> CSV Converter UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.json_csv_converter import json_to_csv, csv_to_json
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_json_csv_converter_view():
    st.markdown("### 🔄 JSON ↔ CSV Converter")
    st.caption("Bidirectional converter between tabular CSV data and JSON array payloads.")
    render_privacy_badge("client_side")

    mode = st.radio("Conversion Direction", ["JSON to CSV", "CSV to JSON"], horizontal=True)

    col_in, col_out = st.columns([1, 1], gap="medium")

    if mode == "JSON to CSV":
        sample = '[{"id": 1, "name": "Alice", "role": "Architect"},\n {"id": 2, "name": "Bob", "role": "Engineer"}]'
        with col_in:
            st.markdown("**JSON Input (Array of Objects)**")
            raw = st.text_area("JSON Input", value=sample, height=240, label_visibility="collapsed")
            delimiter = st.selectbox("Delimiter", [",", ";", "\t"], index=0, format_func=lambda x: "Comma (,)" if x == "," else ("Semicolon (;)" if x == ";" else "Tab (\\t)"))

        with col_out:
            st.markdown("**CSV Output**")
            res = json_to_csv(raw, delimiter=delimiter)
            if not res["success"]:
                render_status_alert(res["error"], "error")
            else:
                st.code(res["output"], language="text")
                st.caption(f"Rows Converted: {res.get('row_count', 0)}")
                st.download_button("📥 Download CSV", data=res["output"], file_name="data.csv", mime="text/csv", use_container_width=True)
    else:
        sample_csv = "id,name,role\n1,Alice,Architect\n2,Bob,Engineer"
        with col_in:
            st.markdown("**CSV Input**")
            raw_csv = st.text_area("CSV Input", value=sample_csv, height=240, label_visibility="collapsed")
            delimiter = st.selectbox("Delimiter", [",", ";", "\t"], index=0, format_func=lambda x: "Comma (,)" if x == "," else ("Semicolon (;)" if x == ";" else "Tab (\\t)"))

        with col_out:
            st.markdown("**JSON Output**")
            res = csv_to_json(raw_csv, delimiter=delimiter)
            if not res["success"]:
                render_status_alert(res["error"], "error")
            else:
                st.code(res["output"], language="json")
                st.caption(f"Records Converted: {res.get('row_count', 0)}")
                st.download_button("📥 Download JSON", data=res["output"], file_name="data.json", mime="application/json", use_container_width=True)
