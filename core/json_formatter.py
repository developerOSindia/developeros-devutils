"""
JSON Formatter Core Module.
Pure Python, standard-library implementation with zero external dependencies.
"""

import json
from typing import Dict, Any

MAX_JSON_BYTES = 2 * 1024 * 1024  # 2 MB Limit


def format_json(
    raw_text: str,
    indent: int = 2,
    sort_keys: bool = False,
    minify: bool = False
) -> Dict[str, Any]:
    """Formats or minifies JSON strings."""
    if raw_text is None:
        return {"output": "", "success": False, "error": "Input cannot be None."}

    data = raw_text.encode("utf-8")
    if len(data) > MAX_JSON_BYTES:
        return {"output": "", "success": False, "error": f"Payload exceeds 2 MB limit ({len(data)} bytes)."}

    stripped = raw_text.strip()
    if not stripped:
        return {"output": "", "success": True, "error": None}

    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as exc:
        return {
            "output": "",
            "success": False,
            "error": f"JSONDecodeError: {exc.msg} (Line {exc.lineno}, Col {exc.colno})",
            "line": exc.lineno,
            "col": exc.colno
        }

    if minify:
        res = json.dumps(parsed, separators=(",", ":"), sort_keys=sort_keys)
    else:
        res = json.dumps(parsed, indent=indent, sort_keys=sort_keys)

    return {
        "output": res,
        "success": True,
        "stats": {
            "original_size": len(stripped),
            "formatted_size": len(res),
            "items_count": len(parsed) if isinstance(parsed, (dict, list)) else 1
        }
    }
