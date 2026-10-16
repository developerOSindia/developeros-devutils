"""
YAML <-> JSON Converter UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.yaml_json_converter import yaml_to_json, json_to_yaml
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_yaml_json_converter_view():
    st.markdown("### 📄 YAML ↔ JSON Converter")
    st.caption("Clean, bidirectional serialization between YAML documents and JSON payloads.")
    render_privacy_badge("client_side")

    mode = st.radio("Conversion Direction", ["YAML to JSON", "JSON to YAML"], horizontal=True)
    col_in, col_out = st.columns([1, 1], gap="medium")

    if mode == "YAML to JSON":
        sample_yaml = "project:\n  name: DeveloperOS\n  tools: 20\n  active: true"
        with col_in:
            st.markdown("**YAML Input**")
            raw = st.text_area("YAML Input", value=sample_yaml, height=240, label_visibility="collapsed")
        with col_out:
            st.markdown("**JSON Output**")
            res = yaml_to_json(raw)
            if not res["success"]:
                render_status_alert(res["error"], "error")
            else:
                st.code(res["output"], language="json")
                st.download_button("📥 Download JSON", data=res["output"], file_name="converted.json", mime="application/json", use_container_width=True)
    else:
        sample_json = '{\n  "project": {\n    "name": "DeveloperOS",\n    "tools": 20,\n    "active": true\n  }\n}'
        with col_in:
            st.markdown("**JSON Input**")
            raw_j = st.text_area("JSON Input", value=sample_json, height=240, label_visibility="collapsed")
        with col_out:
            st.markdown("**YAML Output**")
            res = json_to_yaml(raw_j)
            if not res["success"]:
                render_status_alert(res["error"], "error")
            else:
                st.code(res["output"], language="yaml")
                st.download_button("📥 Download YAML", data=res["output"], file_name="converted.yaml", mime="text/yaml", use_container_width=True)
