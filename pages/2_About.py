"""
DeveloperOS Suite About & Architecture Page.
"""

import sys
from pathlib import Path
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from components.header import render_header
from components.footer import render_footer
from components.privacy import render_privacy_badge

st.set_page_config(page_title="About Suite — DeveloperOS", page_icon="ℹ️", layout="wide")

render_header(suite_title="About Suite", category_badge="Architecture")

st.title("ℹ️ About DeveloperOS Suite")
render_privacy_badge("client_side")

st.markdown("""
### Architecture & Design Philosophy
This application is built on the **DeveloperOS Open-Source Architecture**:
1. **Decoupled Business Logic**: Every utility's computational algorithms reside in `core/` with zero UI framework dependencies.
2. **Modular Tool Plugin Contract**: Tools are self-contained in `tools/` and can be registered or removed without impacting other utilities.
3. **Zero-Trust Ephemeral Privacy**: No user input payloads are ever saved to disk or transmitted to analytics services.
4. **Independent Deployment**: Can be deployed to Streamlit Community Cloud or Docker containers with zero sibling dependencies.

### Useful Links
- [DeveloperOS Main Website](https://developeros.in)
- [DeveloperOS Tools Directory](https://developeros.in/tools)
- [GitHub Organization](https://github.com/developerOSindia)
""")

render_footer()
