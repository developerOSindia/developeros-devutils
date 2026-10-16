"""
Hash Calculator UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.hash_calculator import generate_hashes, generate_hmac, verify_hash, SUPPORTED_ALGORITHMS
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_hash_calculator_view():
    st.markdown("### 🔐 Hash & Checksum Calculator")
    st.caption("Compute multi-algorithm cryptographic hashes, keyed HMAC signatures, and perform timing-safe verification.")
    render_privacy_badge("client_side")

    tab1, tab2, tab3 = st.tabs(["Multi-Hash Digest", "HMAC Generator", "Hash Verifier"])

    with tab1:
        st.markdown("**Input String**")
        input_text = st.text_area("Plain Text to Hash", value="DeveloperOS open-source developer platform", height=120)
        if input_text:
            res = generate_hashes(input_text)
            if res["success"]:
                for algo, hval in res["hashes"].items():
                    with st.container(border=True):
                        st.markdown(f"**{algo}**")
                        st.code(hval, language="text")
            else:
                render_status_alert(res["error"], "error")

    with tab2:
        st.markdown("**HMAC Calculation**")
        hmac_text = st.text_area("Message / Payload", value="transaction_id=98765&amount=100", height=100, key="hmac_txt")
        col_k, col_a = st.columns([2, 1])
        with col_k:
            secret_key = st.text_input("Secret Key", value="my-super-secret-key", type="password")
        with col_a:
            algo_choice = st.selectbox("Algorithm", [a.upper() for a in SUPPORTED_ALGORITHMS], index=0)

        if hmac_text and secret_key:
            hmac_res = generate_hmac(hmac_text, secret_key, algorithm=algo_choice.lower())
            if hmac_res["success"]:
                st.markdown(f"**Computed HMAC ({algo_choice})**")
                st.code(hmac_res["hmac"], language="text")
            else:
                render_status_alert(hmac_res["error"], "error")

    with tab3:
        st.markdown("**Timing-Safe Hash Comparison**")
        col_c, col_e = st.columns(2)
        with col_c:
            cand = st.text_input("Candidate Hash", placeholder="Paste hash A")
        with col_e:
            exp = st.text_input("Expected Hash", placeholder="Paste hash B")

        if cand and exp:
            is_match = verify_hash(cand, exp)
            if is_match:
                render_status_alert("✅ Hashes match exactly (constant-time verified).", "success")
            else:
                render_status_alert("❌ Hashes do NOT match.", "error")
