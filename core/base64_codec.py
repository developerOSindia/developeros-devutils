"""
Base64 Encoder & Decoder Core Module.
Pure Python, standard-library implementation using base64.
"""

import base64
from typing import Dict, Any

MAX_PAYLOAD_BYTES = 5 * 1024 * 1024  # 5 MB Limit


def encode_base64(text: str, url_safe: bool = False) -> Dict[str, Any]:
    """Encodes UTF-8 string into standard or URL-safe Base64."""
    if text is None:
        return {"output": "", "success": False, "error": "Input cannot be None."}

    data = text.encode("utf-8")
    if len(data) > MAX_PAYLOAD_BYTES:
        return {"output": "", "success": False, "error": "Payload exceeds 5 MB limit."}

    if url_safe:
        encoded = base64.urlsafe_b64encode(data).decode("ascii")
    else:
        encoded = base64.b64encode(data).decode("ascii")

    return {
        "output": encoded,
        "success": True,
        "original_len": len(text),
        "encoded_len": len(encoded)
    }


def decode_base64(b64_str: str, url_safe: bool = False) -> Dict[str, Any]:
    """Decodes standard or URL-safe Base64 into UTF-8 text."""
    if not b64_str or not b64_str.strip():
        return {"output": "", "success": True}

    stripped = b64_str.strip()
    data = stripped.encode("ascii", errors="ignore")
    if len(data) > MAX_PAYLOAD_BYTES:
        return {"output": "", "success": False, "error": "Payload exceeds 5 MB limit."}

    try:
        # Normalize padding
        missing_padding = len(stripped) % 4
        if missing_padding:
            stripped += "=" * (4 - missing_padding)

        if url_safe:
            decoded_bytes = base64.urlsafe_b64decode(stripped.encode("ascii"))
        else:
            decoded_bytes = base64.b64decode(stripped.encode("ascii"), validate=True)

        decoded_text = decoded_bytes.decode("utf-8", errors="replace")
        return {"output": decoded_text, "success": True, "bytes_count": len(decoded_bytes)}
    except Exception as exc:
        return {"output": "", "success": False, "error": f"Base64 Decode Error: {str(exc)}"}
