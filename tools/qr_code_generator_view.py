"""
QR Code Generator UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.qr_code_generator import generate_qr_code
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_qr_code_generator_view():
    st.markdown("### 📱 QR Code Generator")
    st.caption("Generate vector SVG and high-resolution PNG QR codes for websites, plain text, and Wi-Fi networks.")
    render_privacy_badge("client_side")

    col_in, col_opts = st.columns([3, 1])
    with col_in:
        payload_text = st.text_input("Content (URL, Text, or Wi-Fi)", value="https://developeros.in")
    with col_opts:
        ec_level = st.selectbox("Error Correction", ["M (15%)", "L (7%)", "Q (25%)", "H (30%)"], index=0)
        ec_choice = ec_level[0]

    if payload_text:
        res = generate_qr_code(payload_text, error_correction=ec_choice)
        if res["success"]:
            col_preview, col_downloads = st.columns([1, 1], gap="medium")
            with col_preview:
                st.markdown("**Rendered QR Code Preview**")
                if res.get("png_bytes"):
                    st.image(res["png_bytes"], width=260)
                elif res.get("svg_content"):
                    st.markdown(res["svg_content"], unsafe_allow_html=True)

            with col_downloads:
                st.markdown("**Export & Downloads**")
                st.caption(f"Payload Size: {res['payload_length']} characters | ECC: Level {res['error_correction']}")

                if res.get("png_bytes"):
                    st.download_button(
                        label="📥 Download PNG Image",
                        data=res["png_bytes"],
                        file_name="qrcode.png",
                        mime="image/png"
                    )

                if res.get("svg_content"):
                    st.download_button(
                        label="📥 Download Vector SVG",
                        data=res["svg_content"],
                        file_name="qrcode.svg",
                        mime="image/svg+xml"
                    )
        else:
            render_status_alert(res["error"], "error")
