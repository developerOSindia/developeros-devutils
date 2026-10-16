"""
Color Converter UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.color_converter import convert_color
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_color_converter_view():
    st.markdown("### 🎨 Color Converter & WCAG Contrast Inspector")
    st.caption("Convert between HEX, RGB, HSL, and CMYK formats, inspect relative luminance, and test accessibility contrast.")
    render_privacy_badge("client_side")

    c_in, c_preset = st.columns([3, 1])
    with c_in:
        color_val = st.text_input("Color String (HEX, RGB, or HSL)", value="#6366f1")
    with c_preset:
        preset = st.selectbox("Palette Presets", ["DeveloperOS Indigo (#6366f1)", "Emerald (#10b981)", "Amber (#f59e0b)", "Rose (#f43f5e)", "Slate (#0f172a)"])
        if preset:
            preset_hex = preset.split("(")[-1].rstrip(")")
            if st.button("Apply Preset"):
                color_val = preset_hex

    if color_val:
        res = convert_color(color_val)
        if res["success"]:
            # Visual Swatch
            st.markdown(
                f"""
                <div style="background-color: {res['hex']}; width: 100%; height: 70px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.2); margin-bottom: 20px; display: flex; align-items: center; justify-content: center;">
                    <span style="color: {'#ffffff' if res['wcag_aa_black'] else '#000000'}; font-weight: bold; font-family: monospace; font-size: 1.1rem;">
                        {res['hex'].upper()}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("HEX Code", res["hex"].upper())
            col2.metric("RGB", res["rgb"])
            col3.metric("HSL", res["hsl"])
            col4.metric("CMYK", res["cmyk"])

            st.markdown("---")
            st.markdown("#### WCAG Accessibility & Contrast Compliance")
            c_w, c_b = st.columns(2)
            with c_w:
                w_status = "✅ PASS (AA)" if res["wcag_aa_white"] else "❌ FAIL"
                st.metric("Contrast against White (#ffffff)", f"{res['contrast_on_white']}:1", w_status)
            with c_b:
                b_status = "✅ PASS (AA)" if res["wcag_aa_black"] else "❌ FAIL"
                st.metric("Contrast against Black (#000000)", f"{res['contrast_on_black']}:1", b_status)

            st.markdown("#### CSS Code Snippet")
            st.code(
                f":root {{\n  --color-primary-hex: {res['hex']};\n  --color-primary-rgb: {res['rgb_tuple'][0]}, {res['rgb_tuple'][1]}, {res['rgb_tuple'][2]};\n  --color-primary-hsl: {res['hsl']};\n}}",
                language="css"
            )
        else:
            render_status_alert(res["error"], "error")
