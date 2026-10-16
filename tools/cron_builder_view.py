"""
Cron Expression Builder & Explainer UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.cron_builder import explain_cron, build_cron, PRESETS
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_cron_builder_view():
    st.markdown("### ⏱️ Cron Expression Builder & Explainer")
    st.caption("Construct, customize, and decode standard 5-part cron schedules into human-readable English.")
    render_privacy_badge("client_side")

    # Mode selector
    tab1, tab2 = st.tabs(["🧩 Visual Builder & Presets", "🔍 Schedule Explainer"])

    with tab1:
        st.markdown("#### Presets & Quick Select")
        preset_choice = st.selectbox(
            "Load Schedule Preset",
            ["Custom", *list(PRESETS.keys())],
            index=0
        )

        preset_val = PRESETS.get(preset_choice, "* * * * *") if preset_choice != "Custom" else "* * * * *"
        preset_parts = preset_val.split()

        st.markdown("#### Individual Fields")
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            min_val = st.text_input("Minute (0-59)", value=preset_parts[0])
        with c2:
            hour_val = st.text_input("Hour (0-23)", value=preset_parts[1])
        with c3:
            dom_val = st.text_input("Day of Month (1-31)", value=preset_parts[2])
        with c4:
            mon_val = st.text_input("Month (1-12)", value=preset_parts[3])
        with c5:
            dow_val = st.text_input("Day of Week (0-6)", value=preset_parts[4])

        built_expr = build_cron(min_val, hour_val, dom_val, mon_val, dow_val)

        st.markdown("#### Resulting Cron Expression")
        st.code(built_expr, language="bash")

        builder_info = explain_cron(built_expr)
        if builder_info["success"]:
            render_status_alert(builder_info["description"], "info")
        else:
            render_status_alert(builder_info["error"], "error")

    with tab2:
        st.markdown("#### Paste & Explain Any Cron Expression")
        user_expr = st.text_input("5-Part Cron Expression", value="*/15 9-17 * * 1-5")
        if user_expr:
            exp_info = explain_cron(user_expr)
            if exp_info["success"]:
                render_status_alert(f"Schedule Meaning: **{exp_info['description']}**", "success")
                st.markdown("**Field Breakdown:**")
                f_cols = st.columns(5)
                fields = exp_info["fields"]
                f_cols[0].metric("Minute", fields["minute"])
                f_cols[1].metric("Hour", fields["hour"])
                f_cols[2].metric("Day of Month", fields["day_of_month"])
                f_cols[3].metric("Month", fields["month"])
                f_cols[4].metric("Day of Week", fields["day_of_week"])
            else:
                render_status_alert(exp_info["error"], "error")
