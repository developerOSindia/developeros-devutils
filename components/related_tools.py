"""
DeveloperOS Related Tools Suggestion Component.
"""

from typing import List
try:
    import streamlit as st
except ImportError:
    st = None


def render_related_tools(tool_ids: List[str], tool_lookup: dict):
    """Renders related tool suggestion cards."""
    if not tool_ids:
        return

    st.markdown("---")
    st.subheader("Related Developer Tools")
    cols = st.columns(min(len(tool_ids), 3))

    for idx, tid in enumerate(tool_ids[:3]):
        info = tool_lookup.get(tid)
        with cols[idx]:
            with st.container(border=True):
                if info:
                    st.markdown(f"**{info.name}**")
                    st.caption(info.description)
                    st.caption(f"Category: `{info.category}`")
                else:
                    st.markdown(f"**{tid}**")
                    st.caption("Standalone utility in DeveloperOS ecosystem.")
