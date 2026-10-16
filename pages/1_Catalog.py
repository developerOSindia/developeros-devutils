"""
DeveloperOS Tools Catalog Page.
Displays the full directory of tools in this suite.
"""

import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools import registry
from components.header import render_header
from components.footer import render_footer

st.set_page_config(page_title="Tools Catalog — DeveloperOS", page_icon="📚", layout="wide")

render_header(suite_title="Tools Catalog", category_badge="Directory")

st.title("📚 Suite Tools Catalog")
st.write("Browse all utilities registered within this DeveloperOS suite.")

search = st.text_input("Filter Catalog", placeholder="Search by name, category, or ID...")
tools = registry.list_all()

if search:
    q = search.lower()
    tools = [t for t in tools if q in t.name.lower() or q in t.category.lower() or q in t.description.lower()]

cols = st.columns(3)
for idx, tool in enumerate(tools):
    with cols[idx % 3]:
        with st.container(border=True):
            st.markdown(f"### {tool.name}")
            st.caption(tool.description)
            st.markdown(f"**Category:** `{tool.category}`")
            st.markdown(f"**Privacy:** `{tool.privacy_classification}`")
            st.markdown(f"**Version:** `{tool.version}`")
            st.markdown(f"**Core Module:** `{tool.core_module}`")

render_footer()
