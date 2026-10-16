"""
XML Formatter & Minifier Core Module.
Pure Python, safe XML formatter using xml.dom.minidom with entity expansion prevention.
"""

import re
import xml.dom.minidom
from typing import Dict, Any

MAX_XML_BYTES = 2 * 1024 * 1024  # 2 MB Limit


def format_xml(xml_str: str, indent: str = "  ", minify: bool = False) -> Dict[str, Any]:
    """Prettifies or minifies XML safely without external entity vulnerability."""
    if not xml_str or not xml_str.strip():
        return {"output": "", "success": True}

    data_bytes = xml_str.encode("utf-8")
    if len(data_bytes) > MAX_XML_BYTES:
        return {"output": "", "success": False, "error": "XML payload exceeds 2 MB limit."}

    # Security check: Disallow external entities and DTD declarations to prevent XXE & Billion Laughs
    if re.search(r"<!ENTITY", xml_str, re.IGNORECASE) or re.search(r"<!DOCTYPE.*\[", xml_str, re.IGNORECASE):
        return {
            "output": "",
            "success": False,
            "error": "Security Alert: DTD entity declarations (XXE) are strictly prohibited."
        }

    stripped = xml_str.strip()
    try:
        dom = xml.dom.minidom.parseString(stripped)
    except Exception as exc:
        return {"output": "", "success": False, "error": f"XML Syntax Error: {str(exc)}"}

    has_declaration = stripped.startswith("<?xml")

    if minify:
        # Minify by removing empty whitespace between tags
        lines = [line.strip() for line in dom.toxml().splitlines() if line.strip()]
        minified = "".join(lines)
        if not has_declaration and minified.startswith("<?xml"):
            minified = re.sub(r"^\<\?xml[^>]+\?\>", "", minified)
        return {"output": minified, "success": True}
    else:
        # Prettify
        pretty = dom.toprettyxml(indent=indent)
        clean_lines = [line for line in pretty.splitlines() if line.strip()]
        if not has_declaration and clean_lines and clean_lines[0].startswith("<?xml"):
            clean_lines = clean_lines[1:]
        return {"output": "\n".join(clean_lines), "success": True}
