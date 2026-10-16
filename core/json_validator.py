"""
JSON Validator & Formatter Core Module.
Pure Python, standard-library implementation using json module.
"""

import json
from typing import Dict, Any

MAX_JSON_BYTES = 2 * 1024 * 1024  # 2 MB Limit


def validate_and_format_json(
    raw_text: str,
    indent: int = 2,
    sort_keys: bool = False,
    minify: bool = False
) -> Dict[str, Any]:
    """Validates, formats, and collects structural statistics on JSON strings."""
    if raw_text is None:
        return {"valid": False, "formatted": "", "error": "Input cannot be None."}

    data_bytes = raw_text.encode("utf-8")
    if len(data_bytes) > MAX_JSON_BYTES:
        return {
            "valid": False,
            "formatted": "",
            "error": f"JSON payload exceeds 2 MB limit ({len(data_bytes)} bytes)."
        }

    stripped = raw_text.strip()
    if not stripped:
        return {
            "valid": False,
            "formatted": "",
            "error": "Input is empty. Please paste valid JSON."
        }

    try:
        parsed = json.loads(stripped)
    except json.JSONDecodeError as exc:
        return {
            "valid": False,
            "formatted": "",
            "error": f"JSONDecodeError: {exc.msg} (Line {exc.lineno}, Column {exc.colno})",
            "line": exc.lineno,
            "column": exc.colno,
            "pos": exc.pos,
        }

    # Statistics
    stats = {
        "root_type": type(parsed).__name__,
        "size_bytes": len(data_bytes),
        "keys_count": len(parsed) if isinstance(parsed, (dict, list)) else 1,
    }

    if minify:
        formatted = json.dumps(parsed, separators=(",", ":"), sort_keys=sort_keys)
    else:
        formatted = json.dumps(parsed, indent=indent, sort_keys=sort_keys)

    return {
        "valid": True,
        "formatted": formatted,
        "stats": stats,
        "original_len": len(stripped),
        "formatted_len": len(formatted),
        "compression_ratio": round(len(formatted) / max(len(stripped), 1), 3),
    }


def validate_json(raw_text: str) -> Dict[str, Any]:
    """Lightweight RFC 8259 syntax validation."""
    res = validate_and_format_json(raw_text)
    return {
        "valid": res["valid"],
        "error": res.get("error"),
        "line": res.get("line"),
        "column": res.get("column"),
        "stats": res.get("stats", {})
    }
