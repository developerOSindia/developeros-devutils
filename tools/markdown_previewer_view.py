"""
Markdown Previewer UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.markdown_previewer import analyze_markdown
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_markdown_previewer_view():
    st.markdown("### 📄 Markdown Live Previewer & Analyzer")
    st.caption("Live rendering of Markdown syntax, table-of-contents extraction, and structural inspection.")
    render_privacy_badge("client_side")

    sample_md = """# DeveloperOS Tools

DeveloperOS is an **offline-first**, modern developer utility platform.

## Features
- Over 20 modular developer tools
- Clean GitHub-ready repositories
- Zero server telemetry

### Quick Links
- [Website](https://developeros.in)
- [Documentation](https://developeros.in/docs)

```python
def hello_developer():
    print("Welcome to DeveloperOS!")
```

> "Empowering developers with secure, offline utilities."
"""

    col_in, col_out = st.columns(2, gap="medium")
    with col_in:
        st.markdown("**Markdown Source Input**")
        md_text = st.text_area("Markdown Text", value=sample_md, height=350, label_visibility="collapsed")

    with col_out:
        st.markdown("**Live Rendered Preview**")
        with st.container(border=True):
            st.markdown(md_text)

    if md_text:
        analysis = analyze_markdown(md_text)
        if analysis["success"]:
            st.markdown("---")
            st.markdown("#### Document Metrics & Outline")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Words", analysis["word_count"])
            m2.metric("Reading Time", f"~{analysis['estimated_reading_minutes']} min")
            m3.metric("Headings", analysis["headings_count"])
            m4.metric("Links / Images", f"{analysis['links_count']} / {analysis['images_count']}")

            if analysis["has_unsafe_html"]:
                render_status_alert(
                    f"Warning: Potentially unsafe raw HTML tags detected ({', '.join(analysis['unsafe_tags_found'])}).",
                    "warning"
                )

            if analysis["headings"]:
                with st.expander("📑 Table of Contents (Outline)", expanded=True):
                    for h in analysis["headings"]:
                        indent = "  " * (h["level"] - 1)
                        st.markdown(f"{indent}- **H{h['level']}**: {h['title']}")
        else:
            render_status_alert(analysis["error"], "error")
