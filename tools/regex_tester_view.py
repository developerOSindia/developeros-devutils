"""
Regex Tester UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.regex_tester import test_regex
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_regex_tester_view():
    st.markdown("### 🔍 Regular Expression Tester")
    st.caption("Test regex patterns against strings, inspect capture groups, and preview substitutions.")
    render_privacy_badge("client_side")

    sample_pattern = r"(?P<protocol>https?)://(?P<host>[a-zA-Z0-9.\-]+)(?P<path>/[^\s]*)"
    sample_text = (
        "Visit our portal at https://developeros.in/tools for free utilities.\n"
        "Legacy mirror available at http://backup.developeros.in/index.html"
    )

    col_pat, col_flags = st.columns([3, 2])
    with col_pat:
        pattern = st.text_input("Regex Pattern", value=sample_pattern)
    with col_flags:
        f1, f2, f3 = st.columns(3)
        ignore_case = f1.checkbox("Ignore Case (i)", value=False)
        multiline = f2.checkbox("Multiline (m)", value=True)
        dot_all = f3.checkbox("DotAll (s)", value=False)

    col_in, col_out = st.columns([1, 1], gap="medium")
    with col_in:
        st.markdown("**Test Text Input**")
        test_text = st.text_area("Test Text", value=sample_text, height=200, label_visibility="collapsed")
        replacement = st.text_input("Optional Replacement String", placeholder="e.g. [REDACTED URL]")

    with col_out:
        st.markdown("**Matches & Evaluation**")
        res = test_regex(
            pattern,
            test_text,
            ignore_case=ignore_case,
            multiline=multiline,
            dot_all=dot_all,
            replacement=replacement if replacement.strip() else None
        )

        if not res["success"]:
            render_status_alert(res["error"], "error")
        else:
            render_status_alert(f"Found {res['match_count']} match(es)!", "success")
            for idx, m in enumerate(res["matches"][:10], start=1):
                with st.container(border=True):
                    st.markdown(f"**Match #{idx}**: `{m['match']}` (Index {m['start']}–{m['end']})")
                    if m["groupdict"]:
                        st.caption(f"Named Groups: {m['groupdict']}")
                    elif m["groups"]:
                        st.caption(f"Capture Groups: {m['groups']}")

            if res.get("replaced_output") is not None:
                st.markdown("**Substitution Output**")
                st.code(res["replaced_output"], language="text")
