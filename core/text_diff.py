"""
Text Diff Checker Core Module.
Pure Python, standard-library implementation using difflib.
"""

import difflib
from typing import Dict, Any, List

MAX_DIFF_CHARS = 500000
MAX_DIFF_LINES = 10000


def compute_text_diff(
    original_text: str,
    modified_text: str,
    diff_type: str = "unified",
    context_lines: int = 3
) -> Dict[str, Any]:
    """Computes textual differences with statistics and unified diff rendering."""
    if original_text is None or modified_text is None:
        return {"success": False, "error": "Original and modified texts cannot be None."}

    if len(original_text) > MAX_DIFF_CHARS or len(modified_text) > MAX_DIFF_CHARS:
        return {"success": False, "error": f"Text exceeds maximum size limit of {MAX_DIFF_CHARS} characters."}

    orig_lines = original_text.splitlines(keepends=True)
    mod_lines = modified_text.splitlines(keepends=True)

    if len(orig_lines) > MAX_DIFF_LINES or len(mod_lines) > MAX_DIFF_LINES:
        return {"success": False, "error": f"Text exceeds maximum line limit of {MAX_DIFF_LINES} lines."}

    # Unified diff
    unified = list(difflib.unified_diff(
        orig_lines,
        mod_lines,
        fromfile="Original",
        tofile="Modified",
        n=context_lines
    ))

    # Calculate additions and deletions
    additions = sum(1 for line in unified if line.startswith("+") and not line.startswith("+++"))
    deletions = sum(1 for line in unified if line.startswith("-") and not line.startswith("---"))

    unified_output = "".join(unified)

    # Detailed line delta opcode breakdown
    matcher = difflib.SequenceMatcher(None, orig_lines, mod_lines)
    ratio = matcher.quick_ratio()

    return {
        "success": True,
        "unified_diff": unified_output,
        "similarity_ratio": round(ratio * 100, 2),
        "additions": additions,
        "deletions": deletions,
        "original_line_count": len(orig_lines),
        "modified_line_count": len(mod_lines),
        "has_changes": additions > 0 or deletions > 0
    }
