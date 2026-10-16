"""
JWT Decoder UI View.
"""

import json
try:
    import streamlit as st
except ImportError:
    st = None

from core.jwt_decoder import decode_jwt
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_jwt_decoder_view():
    st.markdown("### 🪪 JWT Decoder (Header & Payload Inspector)")
    st.caption("Inspect claims, expiration dates, and algorithm headers of JSON Web Tokens.")
    render_privacy_badge("client_side")

    # Security Warning
    st.warning("⚠️ **Security Notice**: This token is decoded client-side only. The cryptographic signature is **NOT verified**. Do not trust claims for authorization without server-side validation.")

    sample_jwt = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkFsaWNlIERldmVsb3BlciIsImlhdCI6MTUxNjIzOTAyMiwiZXhwIjoyMDgwMDAwMDAwfQ."
        "4S_U8gU6qN6vVvYqO0zR7-e0B6d3bE4w1k7yL5n3e9I"
    )

    col_in, col_out = st.columns([1, 1], gap="medium")

    with col_in:
        st.markdown("**Encoded JWT String**")
        token_input = st.text_area("Paste JWT", value=sample_jwt, height=220, label_visibility="collapsed")

    with col_out:
        res = decode_jwt(token_input)
        if not res["success"]:
            render_status_alert(res["error"], "error")
        else:
            st.markdown("**Header**")
            st.code(json.dumps(res["header"], indent=2), language="json")

            st.markdown("**Payload Claims**")
            st.code(json.dumps(res["payload"], indent=2), language="json")

            if res.get("claims_info"):
                st.markdown("**Claim Metadata**")
                info = res["claims_info"]
                if "exp_formatted" in info:
                    status_text = "EXPIRED" if info.get("is_expired") else "VALID / ACTIVE"
                    st.caption(f"Expires: `{info['exp_formatted']}` ({status_text})")
                if "iat_formatted" in info:
                    st.caption(f"Issued At: `{info['iat_formatted']}`")
