"""
CSS Minifier Core Module.
Pure Python, standard-library implementation with zero external dependencies.
Strips comments, eliminates redundant whitespace, removes trailing semicolons.
"""

import re
from typing import Dict, Any

MAX_CSS_LEN = 2 * 1024 * 1024  # 2 MB Limit


def minify_css(
    css_content: str,
    remove_comments: bool = True
) -> Dict[str, Any]:
    """Minifies CSS stylesheet code."""
    if css_content is None:
        return {"output": "", "success": False, "error": "CSS content cannot be None."}

    if len(css_content) > MAX_CSS_LEN:
        return {"output": "", "success": False, "error": f"CSS exceeds maximum size of {MAX_CSS_LEN} bytes."}

    orig_len = len(css_content.encode("utf-8"))
    if not css_content.strip():
        return {
            "output": "",
            "success": True,
            "original_bytes": 0,
            "minified_bytes": 0,
            "savings_percent": 0.0
        }

    text = css_content

    # 1. Remove comments /* ... */
    if remove_comments:
        text = re.sub(r"/\*[\s\S]*?\*/", "", text)

    # 2. Collapse whitespace sequences
    text = re.sub(r"\s+", " ", text)

    # 3. Remove spaces around operators and delimiters
    # { } : ; , > ~ +
    text = re.sub(r"\s*([\{\}:;,>~+])\s*", r"\1", text)

    # 4. Remove unnecessary trailing semicolon before }
    text = re.sub(r";\}", "}", text)

    # 5. Remove empty rulesets like .class{}
    text = re.sub(r"[^{}]+\{\}", "", text)

    minified_css = text.strip()
    min_len = len(minified_css.encode("utf-8"))
    savings = max(0.0, round(((orig_len - min_len) / orig_len * 100), 2)) if orig_len > 0 else 0.0

    return {
        "output": minified_css,
        "success": True,
        "original_bytes": orig_len,
        "minified_bytes": min_len,
        "saved_bytes": max(0, orig_len - min_len),
        "savings_percent": savings
    }
