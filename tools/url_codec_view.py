"""
URL Encoder, Decoder & Parser UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.url_codec import encode_url, decode_url, parse_url_components
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_url_codec_view():
    st.markdown("### 🔗 URL Encoder, Decoder & Inspector")
    st.caption("Safely encode or decode URL query strings and inspect protocol/path/query components.")
    render_privacy_badge("client_side")

    tab1, tab2, tab3 = st.tabs(["Encode URL", "Decode URL", "Inspect & Parse URL"])

    sample_query = "search query=developer tools & ecosystem=DeveloperOS 2026/v1.0"
    sample_url = "https://developeros.in:443/tools?category=security&format=json#overview"

    with tab1:
        st.markdown("**Input Plain Text**")
        raw_text = st.text_area("Plain Text to Encode", value=sample_query, height=120)
        plus_space = st.checkbox("Encode spaces as `+` (application/x-www-form-urlencoded)", value=True, key="enc_plus")

        if raw_text:
            res_enc = encode_url(raw_text, plus_spaces=plus_space)
            if res_enc["success"]:
                st.markdown("**Encoded Output**")
                st.code(res_enc["output"], language="text")
                st.caption(f"Original length: {res_enc['original_len']} chars | Encoded: {res_enc['encoded_len']} chars")
            else:
                render_status_alert(res_enc["error"], "error")

    with tab2:
        st.markdown("**Input Encoded String**")
        enc_input = st.text_area("URL to Decode", value="search+query%3Ddeveloper+tools+%26+ecosystem%3DDeveloperOS+2026%2Fv1.0", height=120)
        dec_plus = st.checkbox("Decode `+` as space", value=True, key="dec_plus")

        if enc_input:
            res_dec = decode_url(enc_input, plus_spaces=dec_plus)
            if res_dec["success"]:
                st.markdown("**Decoded Output**")
                st.code(res_dec["output"], language="text")
            else:
                render_status_alert(res_dec["error"], "error")

    with tab3:
        st.markdown("**URL Component Inspector**")
        parse_input = st.text_input("Enter Full URL", value=sample_url)
        if parse_input:
            parsed = parse_url_components(parse_input)
            if parsed["success"]:
                c1, c2, c3 = st.columns(3)
                c1.metric("Scheme", parsed["scheme"] or "None")
                c2.metric("Hostname", parsed["hostname"] or "None")
                c3.metric("Port", str(parsed["port"]) if parsed["port"] else "Default")

                st.markdown("**Path & Fragment**")
                st.code(f"Path:     {parsed['path']}\nFragment: {parsed['fragment']}", language="text")

                if parsed["query_params"]:
                    st.markdown("**Parsed Query Parameters**")
                    st.json(parsed["query_params"])
            else:
                render_status_alert(parsed["error"], "error")
