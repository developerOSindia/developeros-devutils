"""
JSON <-> CSV Converter Core Module.
Pure Python, standard-library implementation using json, csv, and io.
"""

import csv
import io
import json
from typing import Dict, Any

MAX_PAYLOAD_BYTES = 2 * 1024 * 1024  # 2 MB Limit


def json_to_csv(json_str: str, delimiter: str = ",") -> Dict[str, Any]:
    """Converts a JSON list of objects into a CSV string."""
    if not json_str or not json_str.strip():
        return {"output": "", "success": True, "row_count": 0}

    data_bytes = json_str.encode("utf-8")
    if len(data_bytes) > MAX_PAYLOAD_BYTES:
        return {"output": "", "success": False, "error": "Payload exceeds 2 MB limit."}

    try:
        parsed = json.loads(json_str.strip())
    except json.JSONDecodeError as exc:
        return {"output": "", "success": False, "error": f"Invalid JSON: {exc.msg} (Line {exc.lineno})"}

    if isinstance(parsed, dict):
        parsed = [parsed]
    elif not isinstance(parsed, list):
        return {"output": "", "success": False, "error": "JSON root must be an array of objects or an object."}

    if not parsed:
        return {"output": "", "success": True, "row_count": 0}

    # Extract all unique keys across all records
    headers = []
    for item in parsed:
        if isinstance(item, dict):
            for k in item.keys():
                if k not in headers:
                    headers.append(k)

    if not headers:
        return {"output": "", "success": False, "error": "No object keys found to construct CSV columns."}

    out_io = io.StringIO()
    writer = csv.DictWriter(out_io, fieldnames=headers, delimiter=delimiter, lineterminator="\n")
    writer.writeheader()

    count = 0
    for row in parsed:
        if isinstance(row, dict):
            # Flatten non-primitive fields to JSON strings
            sanitized = {k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in row.items()}
            writer.writerow(sanitized)
            count += 1

    return {"output": out_io.getvalue(), "success": True, "row_count": count, "headers": headers}


def csv_to_json(csv_str: str, delimiter: str = ",", indent: int = 2) -> Dict[str, Any]:
    """Converts a CSV string into a JSON array of objects."""
    if not csv_str or not csv_str.strip():
        return {"output": "[]", "success": True, "row_count": 0}

    data_bytes = csv_str.encode("utf-8")
    if len(data_bytes) > MAX_PAYLOAD_BYTES:
        return {"output": "", "success": False, "error": "Payload exceeds 2 MB limit."}

    try:
        in_io = io.StringIO(csv_str.strip())
        reader = csv.DictReader(in_io, delimiter=delimiter)
        rows = []
        for r in reader:
            parsed_row = {}
            for k, v in r.items():
                if k is None:
                    continue
                # Auto-cast numbers/booleans where clean
                val = v.strip() if v else ""
                if val.lower() == "true":
                    parsed_row[k] = True
                elif val.lower() == "false":
                    parsed_row[k] = False
                elif val.isdigit():
                    parsed_row[k] = int(val)
                else:
                    try:
                        parsed_row[k] = float(val) if "." in val else val
                    except ValueError:
                        parsed_row[k] = val
            rows.append(parsed_row)

        output_json = json.dumps(rows, indent=indent)
        return {"output": output_json, "success": True, "row_count": len(rows)}
    except Exception as exc:
        return {"output": "", "success": False, "error": f"CSV parse error: {str(exc)}"}
