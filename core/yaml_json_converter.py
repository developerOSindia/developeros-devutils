"""
YAML <-> JSON Converter Core Module.
Pure Python, safe YAML parser and JSON serializer.
"""

import json
from typing import Dict, Any

try:
    import yaml
except ImportError:
    yaml = None

MAX_PAYLOAD_BYTES = 2 * 1024 * 1024  # 2 MB Limit


def yaml_to_json(yaml_str: str, indent: int = 2, sort_keys: bool = False) -> Dict[str, Any]:
    """Converts YAML input into formatted JSON string."""
    if not yaml_str or not yaml_str.strip():
        return {"output": "{}", "success": True}

    data_bytes = yaml_str.encode("utf-8")
    if len(data_bytes) > MAX_PAYLOAD_BYTES:
        return {"output": "", "success": False, "error": "Payload exceeds 2 MB limit."}

    if yaml is None:
        return {"output": "", "success": False, "error": "PyYAML package is not installed."}

    try:
        parsed = yaml.safe_load(yaml_str)
        formatted = json.dumps(parsed, indent=indent, sort_keys=sort_keys)
        return {"output": formatted, "success": True}
    except Exception as exc:
        return {"output": "", "success": False, "error": f"YAML parsing error: {str(exc)}"}


def json_to_yaml(json_str: str, indent: int = 2) -> Dict[str, Any]:
    """Converts JSON input into clean YAML string."""
    if not json_str or not json_str.strip():
        return {"output": "", "success": True}

    data_bytes = json_str.encode("utf-8")
    if len(data_bytes) > MAX_PAYLOAD_BYTES:
        return {"output": "", "success": False, "error": "Payload exceeds 2 MB limit."}

    try:
        parsed = json.loads(json_str)
    except json.JSONDecodeError as exc:
        return {"output": "", "success": False, "error": f"Invalid JSON: {exc.msg} (Line {exc.lineno})"}

    if yaml is None:
        return {"output": "", "success": False, "error": "PyYAML package is not installed."}

    try:
        formatted = yaml.safe_dump(parsed, sort_keys=False, indent=indent, allow_unicode=True)
        return {"output": formatted, "success": True}
    except Exception as exc:
        return {"output": "", "success": False, "error": f"YAML dump error: {str(exc)}"}
