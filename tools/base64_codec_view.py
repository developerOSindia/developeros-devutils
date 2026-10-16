"""
Base64 Encoder & Decoder UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.base64_codec import encode_base64, decode_base64
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_base64_codec_view():
    st.markdown("### 🔤 Base64 Encoder / Decoder")
    st.caption("Encode plain text into Base64 format or decode Base64 back into readable text.")
    render_privacy_badge("client_side")

    action = st.radio("Action Mode", ["Encode to Base64", "Decode from Base64"], horizontal=True)
    url_safe = st.checkbox("URL-Safe Base64 (replace + and / with - and _)", value=False)

    col_in, col_out = st.columns([1, 1], gap="medium")

    if action == "Encode to Base64":
        with col_in:
            st.markdown("**Plain Text Input**")
            raw = st.text_area("Input Text", value="Hello, DeveloperOS 2026!", height=240, label_visibility="collapsed")
        with col_out:
            st.markdown("**Base64 Encoded Output**")
            res = encode_base64(raw, url_safe=url_safe)
            if not res["success"]:
                render_status_alert(res["error"], "error")
            else:
                st.text_area("Output", value=res["output"], height=240, label_visibility="collapsed")
                st.caption(f"Input: {res['original_len']} chars | Output: {res['encoded_len']} chars")
                st.download_button("📥 Download Encoded Text", data=res["output"], file_name="encoded_base64.txt", mime="text/plain", use_container_width=True)
    else:
        with col_in:
            st.markdown("**Base64 Encoded Input**")
            raw_b64 = st.text_area("Input Base64", value="SGVsbG8sIERldmVsb3Blck9TIDIwMjYh", height=240, label_visibility="collapsed")
        with col_out:
            st.markdown("**Decoded UTF-8 Output**")
            res = decode_base64(raw_b64, url_safe=url_safe)
            if not res["success"]:
                render_status_alert(res["error"], "error")
            else:
                st.text_area("Output", value=res["output"], height=240, label_visibility="collapsed")
                st.download_button("📥 Download Decoded Text", data=res["output"], file_name="decoded_text.txt", mime="text/plain", use_container_width=True)
