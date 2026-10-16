"""
Hash & HMAC Generator UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None
from core.hash_generator import generate_hashes, generate_hmac, verify_hash
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_hash_generator_view():
    """Renders the Multi-Algorithm Hasher & HMAC Generator tool UI."""
    st.markdown("### 🔐 Multi-Algorithm Hasher & HMAC")
    st.caption("Generate SHA-256, SHA-512, MD5 hashes, and HMAC digests.")
    render_privacy_badge("client_side")

    col_in, col_out = st.columns([1, 1], gap="medium")

    with col_in:
        st.markdown("**Input String**")
        input_text = st.text_area(
            "Text to hash",
            value="DeveloperOS-Open-Source-2026",
            height=140,
            label_visibility="collapsed"
        )
        st.markdown("**Optional HMAC Secret Key**")
        hmac_key = st.text_input(
            "Secret Key",
            type="password",
            placeholder="Enter key to generate HMAC..."
        )

        st.markdown("**Hash Verification Check**")
        candidate_hash = st.text_input(
            "Candidate Hash to Verify",
            placeholder="Paste expected hash to compare..."
        )

    with col_out:
        st.markdown("**Computed Cryptographic Hashes**")
        result = generate_hashes(input_text)

        if not result["success"]:
            render_status_alert(result["error"], "error")
            return

        hashes = result["hashes"]
        output_lines = []
        for algo, val in hashes.items():
            st.markdown(f"**{algo}**")
            st.code(val, language="text")
            output_lines.append(f"{algo}: {val}")

        if hmac_key.strip():
            hmac_res = generate_hmac(input_text, hmac_key, "sha256")
            if hmac_res["success"]:
                st.markdown("**HMAC (SHA-256)**")
                st.code(hmac_res["hmac"], language="text")
                output_lines.append(f"HMAC-SHA256: {hmac_res['hmac']}")

        if candidate_hash.strip():
            matched_algo = None
            for algo, val in hashes.items():
                if verify_hash(candidate_hash, val):
                    matched_algo = algo
                    break
            if matched_algo:
                render_status_alert(f"Match confirmed! Matches {matched_algo} digest.", "success")
            else:
                render_status_alert("No match. Candidate does not match any computed digest.", "warning")

        st.download_button(
            "📥 Download Hashes",
            data="\n".join(output_lines),
            file_name="computed_hashes.txt",
            mime="text/plain",
            use_container_width=True
        )
