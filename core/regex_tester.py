"""
Regex Tester Core Module.
Pure Python, safe regular expression evaluator with bounded execution and ReDoS limits.
"""

import re
from typing import Dict, Any, List

MAX_PATTERN_LEN = 500
MAX_TEXT_LEN = 100000
MAX_MATCH_LIMIT = 500


def test_regex(
    pattern: str,
    test_text: str,
    ignore_case: bool = False,
    multiline: bool = False,
    dot_all: bool = False,
    replacement: str | None = None
) -> Dict[str, Any]:
    """Safely tests regex pattern against string with match limits."""
    if not pattern:
        return {"success": False, "error": "Pattern cannot be empty."}

    if len(pattern) > MAX_PATTERN_LEN:
        return {"success": False, "error": f"Pattern exceeds safety limit of {MAX_PATTERN_LEN} characters."}

    if test_text is None:
        return {"success": False, "error": "Test text cannot be None."}

    if len(test_text) > MAX_TEXT_LEN:
        return {"success": False, "error": f"Test text exceeds safety limit of {MAX_TEXT_LEN} characters."}

    flags = 0
    if ignore_case:
        flags |= re.IGNORECASE
    if multiline:
        flags |= re.MULTILINE
    if dot_all:
        flags |= re.DOTALL

    try:
        compiled = re.compile(pattern, flags)
    except re.error as exc:
        return {"success": False, "error": f"Regex Syntax Error: {str(exc)}"}

    matches: List[Dict[str, Any]] = []
    count = 0
    for m in compiled.finditer(test_text):
        count += 1
        if count <= MAX_MATCH_LIMIT:
            matches.append({
                "match": m.group(0),
                "start": m.start(),
                "end": m.end(),
                "groups": list(m.groups()),
                "groupdict": m.groupdict()
            })
        else:
            break

    replaced_output = None
    if replacement is not None:
        try:
            replaced_output = compiled.sub(replacement, test_text)
        except Exception as exc:
            return {"success": False, "error": f"Substitution Error: {str(exc)}"}

    return {
        "success": True,
        "match_count": count,
        "matches": matches,
        "is_truncated": count > MAX_MATCH_LIMIT,
        "replaced_output": replaced_output
    }
