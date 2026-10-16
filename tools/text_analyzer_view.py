"""
Text Analyzer & Metrics UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None
from core.text_analyzer import analyze_text, transform_text_case
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_text_analyzer_view():
    """Renders the Text Analyzer interactive tool UI."""
    st.markdown("### 📝 Text Analyzer & Readability Metrics")
    st.caption("Inspect text density, word counts, reading duration, and Shannon entropy.")
    render_privacy_badge("client_side")

    col_in, col_out = st.columns([1, 1], gap="medium")

    with col_in:
        st.markdown("**Input Text**")
        sample_text = (
            "DeveloperOS is an open-source tools ecosystem built for engineers.\n"
            "All utilities process data client-side with zero retention and maximum speed."
        )
        user_text = st.text_area(
            "Paste text to analyze",
            value=sample_text,
            height=240,
            label_visibility="collapsed"
        )
        transform_mode = st.selectbox(
            "Case Transformation",
            ["None", "UPPER", "lower", "Title", "snake", "kebab", "camel"],
            index=0
        )

    with col_out:
        st.markdown("**Calculated Metrics**")
        metrics = analyze_text(user_text)

        if not metrics.success:
            render_status_alert(metrics.error or "Analysis error", "error")
            return

        m_col1, m_col2, m_col3 = st.columns(3)
        m_col1.metric("Characters", f"{metrics.total_chars:,}")
        m_col2.metric("Words", f"{metrics.total_words:,}")
        m_col3.metric("Reading Time", f"{metrics.reading_time_sec}s")

        e_col1, e_col2, e_col3 = st.columns(3)
        e_col1.metric("Lines", metrics.total_lines)
        e_col2.metric("Sentences", metrics.total_sentences)
        e_col3.metric("Shannon Entropy", f"{metrics.shannon_entropy} bits")

        transformed_content = user_text
        if transform_mode != "None":
            res = transform_text_case(user_text, transform_mode)
            if res["success"]:
                transformed_content = res["output"]

        st.markdown("**Transformed Text Output**")
        st.text_area(
            "Output",
            value=transformed_content,
            height=120,
            label_visibility="collapsed"
        )

        st.download_button(
            "📥 Download Output",
            data=transformed_content,
            file_name="analyzed_text.txt",
            mime="text/plain",
            use_container_width=True
        )
