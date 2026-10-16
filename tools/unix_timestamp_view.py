"""
Unix Timestamp Converter UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

import time
from core.unix_timestamp import timestamp_to_datetimes, datetime_to_timestamp, get_current_timestamp
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_unix_timestamp_view():
    st.markdown("### 🕒 Unix Timestamp Converter")
    st.caption("Convert epoch seconds or milliseconds to human-readable UTC/local times, and parse dates back to timestamps.")
    render_privacy_badge("client_side")

    curr = get_current_timestamp()

    # Quick current timestamp badge
    st.info(f"⚡ Current Epoch: **{curr['seconds']}** (seconds) | **{curr['milliseconds']}** (ms) | UTC: `{curr['iso_8601']}`")

    tab1, tab2 = st.tabs(["🔢 Timestamp → Human Date", "📅 Human Date → Timestamp"])

    with tab1:
        c1, c2 = st.columns([3, 1])
        with c1:
            ts_input = st.text_input("Epoch Timestamp", value=str(curr["seconds"]))
        with c2:
            is_ms = st.checkbox("Is Milliseconds?", value=False)

        if ts_input.strip():
            try:
                res = timestamp_to_datetimes(ts_input, is_millis=is_ms)
                if res["success"]:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.markdown("**UTC Representation**")
                        st.code(res["utc_string"], language="text")
                        st.markdown("**Local Timezone**")
                        st.code(res["local_string"], language="text")
                    with col_b:
                        st.markdown("**ISO 8601**")
                        st.code(res["iso_8601"], language="text")
                        st.markdown("**RFC 2822**")
                        st.code(res["rfc_2822"], language="text")

                    st.markdown(f"**Relative Time:** `{res['relative']}`")
                else:
                    render_status_alert(res["error"], "error")
            except Exception as e:
                render_status_alert(f"Conversion error: {str(e)}", "error")

    with tab2:
        dt_input = st.text_input("Date/Time String (ISO 8601 or YYYY-MM-DD HH:MM:SS)", value="2026-10-16 12:00:00")
        if dt_input.strip():
            res_dt = datetime_to_timestamp(dt_input)
            if res_dt["success"]:
                r_col1, r_col2 = st.columns(2)
                r_col1.metric("Seconds", str(res_dt["seconds"]))
                r_col2.metric("Milliseconds", str(res_dt["milliseconds"]))
                st.code(f"Seconds: {res_dt['seconds']}\nMillis:  {res_dt['milliseconds']}", language="bash")
            else:
                render_status_alert(res_dt["error"], "error")
