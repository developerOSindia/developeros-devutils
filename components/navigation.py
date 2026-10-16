"""
DeveloperOS Navigation & Tool Filtering Component.
"""

from typing import List, Tuple, Optional
try:
    import streamlit as st
except ImportError:
    st = None


def render_tool_navigation(categories: List[str], tools: list) -> Tuple[Optional[str], Optional[object]]:
    """Renders category filter pills, search input, and tool selector."""
    with st.sidebar:
        st.markdown("### 🛠️ Tool Selection")
        search_query = st.text_input("🔍 Search Tools", placeholder="Filter by name or tag...")

        selected_category = st.selectbox("📂 Category", ["All Categories"] + sorted(categories))

        # Filter tools
        filtered = tools
        if selected_category != "All Categories":
            filtered = [t for t in filtered if t.category == selected_category]
        if search_query.strip():
            q = search_query.strip().lower()
            filtered = [t for t in filtered if q in t.name.lower() or q in t.description.lower() or q in t.id.lower()]

        if not filtered:
            st.warning("No tools match your search criteria.")
            return None, None

        tool_names = [t.name for t in filtered]
        chosen_name = st.radio("Available Tools", tool_names, index=0)
        chosen_tool = next(t for t in filtered if t.name == chosen_name)

        st.markdown("---")
        st.markdown(f"**Version**: `{chosen_tool.version}`")
        st.markdown(f"**Privacy**: `{chosen_tool.privacy_classification}`")
        if chosen_tool.documentation_link:
            st.markdown(f"[📖 Documentation]({chosen_tool.documentation_link})")

    return chosen_name, chosen_tool
