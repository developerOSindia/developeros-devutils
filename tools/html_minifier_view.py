"""
HTML Minifier UI View.
"""

try:
    import streamlit as st
except ImportError:
    st = None

from core.html_minifier import minify_html
from components.privacy import render_privacy_badge
from components.alerts import render_status_alert


def render_html_minifier_view():
    st.markdown("### 🌐 HTML Minifier")
    st.caption("Compress HTML payloads, strip unnecessary whitespace and comments, and accelerate page render times.")
    render_privacy_badge("client_side")

    sample_html = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <!-- Main page title -->
    <title>DeveloperOS Tools</title>
  </head>
  <body>
    <header class="navbar">
      <h1>DeveloperOS Ecosystem</h1>
    </header>
    <main>
      <p>Secure, client-side developer utilities.</p>
      <pre>
        <code>
          function keepFormatting() {
              return true;
          }
        </code>
      </pre>
    </main>
  </body>
</html>"""

    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        rm_comments = st.checkbox("Strip HTML Comments", value=True)
    with col_opt2:
        collapse_ws = st.checkbox("Collapse Whitespace", value=True)

    col_in, col_out = st.columns(2, gap="medium")
    with col_in:
        st.markdown("**Raw HTML Source**")
        raw_html = st.text_area("HTML Input", value=sample_html, height=300, label_visibility="collapsed")

    with col_out:
        st.markdown("**Minified Output**")
        if raw_html:
            res = minify_html(raw_html, remove_comments=rm_comments, collapse_whitespace=collapse_ws)
            if res["success"]:
                st.text_area("Minified HTML", value=res["output"], height=300, label_visibility="collapsed")
                st.download_button(
                    label="📥 Download Minified HTML",
                    data=res["output"],
                    file_name="index.min.html",
                    mime="text/html"
                )
            else:
                render_status_alert(res["error"], "error")

    if raw_html and res.get("success"):
        st.markdown("---")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Original Size", f"{res['original_bytes']} B")
        m2.metric("Minified Size", f"{res['minified_bytes']} B")
        m3.metric("Bytes Saved", f"{res['saved_bytes']} B")
        m4.metric("Compression Ratio", f"{res['savings_percent']}%")
