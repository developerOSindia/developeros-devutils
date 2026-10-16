"""
Text Case Converter UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.text_case_converter import convert_cases
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_text_case_converter_view():
    st.markdown("### 🔤 Text Case Converter")
    st.caption("Transform strings, variable names, and identifiers across camelCase, snake_case, PascalCase, and kebab-case.")
    render_privacy_badge("client_side")

    input_text = st.text_input("Enter text to convert", value="DeveloperOS open-source software tools")

    if input_text:
        res = convert_cases(input_text)
        if res["success"]:
            st.markdown("#### Programmatic & Typographic Conversions")

            cases_display = [
                ("camelCase", res["camel_case"]),
                ("PascalCase", res["pascal_case"]),
                ("snake_case", res["snake_case"]),
                ("CONSTANT_CASE", res["constant_case"]),
                ("kebab-case", res["kebab_case"]),
                ("COBOL-CASE", res["cobol_case"]),
                ("dot.case", res["dot_case"]),
                ("path/case", res["path_case"]),
                ("Title Case", res["title_case"]),
                ("lowercase", res["lowercase"]),
                ("UPPERCASE", res["uppercase"]),
                ("Sentence case", res["sentence_case"]),
            ]

            col1, col2 = st.columns(2)
            for idx, (label, val) in enumerate(cases_display):
                target_col = col1 if idx % 2 == 0 else col2
                with target_col:
                    with st.container(border=True):
                        st.caption(f"**{label}**")
                        st.code(val, language="text")
        else:
            render_status_alert(res["error"], "error")
