"""
HTML Minifier Core Module.
Pure Python, standard-library implementation with zero external dependencies.
Safely collapses whitespace and removes comments while preserving pre/code/script tags.
"""

import re
from typing import Dict, Any

MAX_HTML_LEN = 2 * 1024 * 1024  # 2 MB Limit


def minify_html(
    html_content: str,
    remove_comments: bool = True,
    collapse_whitespace: bool = True
) -> Dict[str, Any]:
    """Minifies HTML markup while preserving sensitive blocks like pre, code, and textarea."""
    if html_content is None:
        return {"output": "", "success": False, "error": "HTML content cannot be None."}

    if len(html_content) > MAX_HTML_LEN:
        return {"output": "", "success": False, "error": f"HTML content exceeds maximum size of {MAX_HTML_LEN} bytes."}

    orig_len = len(html_content.encode("utf-8"))
    if not html_content.strip():
        return {
            "output": "",
            "success": True,
            "original_bytes": 0,
            "minified_bytes": 0,
            "savings_percent": 0.0
        }

    # Protect <pre>, <code>, <textarea>, and <script> contents with placeholders
    preserved_blocks: Dict[str, str] = {}

    def _preserve_tag(match):
        key = f"__DEVOS_PRESERVE_{len(preserved_blocks)}__"
        preserved_blocks[key] = match.group(0)
        return key

    # Regex matching tags that require literal whitespace preservation
    protect_pattern = re.compile(
        r"<(pre|code|textarea|script|style)\b[^>]*>[\s\S]*?<\/\1>",
        re.IGNORECASE
    )
    working_text = protect_pattern.sub(_preserve_tag, html_content)

    # 1. Remove comments if requested (preserve conditional comments like <!--[if ...)
    if remove_comments:
        working_text = re.sub(r"<!--(?!\[if)[\s\S]*?-->", "", working_text)

    # 2. Collapse inter-tag whitespace
    if collapse_whitespace:
        # Collapse whitespace between tags: > \s+ < -> ><
        working_text = re.sub(r">\s+<", "><", working_text)
        # Collapse multi-space and tabs into single space
        working_text = re.sub(r"[ \t\r\n]+", " ", working_text)

    # Restore preserved blocks
    for key, original_block in preserved_blocks.items():
        working_text = working_text.replace(key, original_block)

    minified_text = working_text.strip()
    min_len = len(minified_text.encode("utf-8"))
    savings = max(0.0, round(((orig_len - min_len) / orig_len * 100), 2)) if orig_len > 0 else 0.0

    return {
        "output": minified_text,
        "success": True,
        "original_bytes": orig_len,
        "minified_bytes": min_len,
        "saved_bytes": max(0, orig_len - min_len),
        "savings_percent": savings
    }
