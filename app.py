"""
DeveloperOS Streamlit Suite Main Application Entrypoint.
Orchestrates tool navigation, category filtering, shared branding, and error isolation.
"""

import sys
from pathlib import Path
try:
    import streamlit as st
except ImportError:
    st = None

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from tools import registry
from components.header import render_header
from components.footer import render_footer
from components.banner import render_main_promotional_banner
from components.navigation import render_tool_navigation
from components.related_tools import render_related_tools
from components.alerts import render_status_alert

# Streamlit Page Configuration
if st is not None:
    st.set_page_config(
        page_title="DeveloperOS Tools Suite",
        page_icon="🛠️",
        layout="wide",
        initial_sidebar_state="expanded"
    )


def load_suite_metadata() -> dict:
    """Safely loads suite metadata from manifest.yaml or defaults."""
    manifest_path = PROJECT_ROOT / "manifest.yaml"
    if manifest_path.exists():
        try:
            import yaml
            with open(manifest_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            pass
    return {
        "name": "DeveloperOS Tools Suite",
        "category": "Utilities",
        "repository": "https://github.com/developerOSindia"
    }


def main():
    if st is None:
        print("DeveloperOS Tools Suite: Streamlit is required to launch the interactive web UI.")
        print("Install dependencies and run: pip install -r requirements.txt && streamlit run app.py")
        return

    metadata = load_suite_metadata()
    suite_title = metadata.get("name", "DeveloperOS Tools Suite")
    suite_category = metadata.get("category", "Utilities")
    repo_url = metadata.get("repository", "https://github.com/developerOSindia")

    # 1. Render Top Header
    render_header(
        suite_title=suite_title,
        category_badge=suite_category,
        github_repo=repo_url
    )

    # 2. Tool Navigation
    all_tools = registry.list_all()
    categories = registry.get_categories()

    if not all_tools:
        render_status_alert("No developer tools are currently registered in this suite.", "warning")
        render_footer()
        return

    chosen_name, chosen_tool = render_tool_navigation(categories, all_tools)

    if not chosen_tool:
        st.info("Select a utility from the sidebar to begin.")
        render_footer()
        return

    # 3. Safe Tool Execution
    try:
        chosen_tool.ui_entrypoint()
    except Exception as exc:
        render_status_alert(f"An unexpected error occurred while running {chosen_tool.name}: {exc}", "error")

    # 4. Related Tools Recommendations
    tool_lookup = {t.id: t for t in all_tools}
    if chosen_tool.related_tools:
        render_related_tools(chosen_tool.related_tools, tool_lookup)

    # 5. Universal Promotional Banner (below primary tool interface)
    render_main_promotional_banner(tool_name=chosen_tool.name)

    # 6. Render Standard Footer Banner
    render_footer()


if __name__ == "__main__":
    main()
