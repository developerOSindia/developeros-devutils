"""
UUID Generator UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.uuid_generator import generate_uuids
from components.privacy import render_privacy_badge


def render_uuid_generator_view():
    st.markdown("### 🆔 UUID Generator")
    st.caption("Generate cryptographically random UUIDv4 or time-based UUIDv1 identifiers.")
    render_privacy_badge("client_side")

    c1, c2, c3, c4 = st.columns(4)
    count = c1.slider("Quantity", 1, 50, 5)
    version = c2.selectbox("UUID Version", [4, 1], format_func=lambda v: f"Version {v} ({'Random' if v==4 else 'Time-based'})")
    uppercase = c3.checkbox("Uppercase", value=False)
    hyphens = c4.checkbox("Hyphens", value=True)

    if st.button("Generate UUIDs", type="primary"):
        st.session_state["devutils_last_uuids"] = generate_uuids(count, version=version, uppercase=uppercase, hyphens=hyphens)["uuids"]

    if "devutils_last_uuids" not in st.session_state:
        st.session_state["devutils_last_uuids"] = generate_uuids(count, version=version, uppercase=uppercase, hyphens=hyphens)["uuids"]

    uuids = st.session_state["devutils_last_uuids"]
    output_text = "\n".join(uuids)

    st.code(output_text, language="text")

    st.download_button(
        "📥 Download UUIDs",
        data=output_text,
        file_name="uuids.txt",
        mime="text/plain",
        use_container_width=True
    )
