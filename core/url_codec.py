"""
URL Encoder, Decoder & Parser Core Module.
Pure Python, standard-library implementation using urllib.parse.
"""

import urllib.parse
from typing import Dict, Any

MAX_URL_LEN = 100000


def encode_url(text: str, plus_spaces: bool = True) -> Dict[str, Any]:
    """Encodes string into URL percent-encoded format."""
    if text is None:
        return {"success": False, "error": "Input cannot be None."}

    if len(text) > MAX_URL_LEN:
        return {"success": False, "error": f"Input exceeds maximum allowed length of {MAX_URL_LEN} characters."}

    try:
        if plus_spaces:
            encoded = urllib.parse.quote_plus(text)
        else:
            encoded = urllib.parse.quote(text)

        return {
            "success": True,
            "output": encoded,
            "original_len": len(text),
            "encoded_len": len(encoded)
        }
    except Exception as exc:
        return {"success": False, "error": f"URL Encoding Error: {str(exc)}"}


def decode_url(text: str, plus_spaces: bool = True) -> Dict[str, Any]:
    """Decodes URL percent-encoded string back to raw text."""
    if text is None:
        return {"success": False, "error": "Input cannot be None."}

    if len(text) > MAX_URL_LEN:
        return {"success": False, "error": f"Input exceeds maximum allowed length of {MAX_URL_LEN} characters."}

    try:
        if plus_spaces:
            decoded = urllib.parse.unquote_plus(text)
        else:
            decoded = urllib.parse.unquote(text)

        return {
            "success": True,
            "output": decoded,
            "decoded_len": len(decoded)
        }
    except Exception as exc:
        return {"success": False, "error": f"URL Decoding Error: {str(exc)}"}


def parse_url_components(url_str: str) -> Dict[str, Any]:
    """Deconstructs a URL into its structural components and query parameters."""
    if not url_str or not url_str.strip():
        return {"success": False, "error": "URL cannot be empty."}

    try:
        parsed = urllib.parse.urlsplit(url_str.strip())
        query_dict = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)

        return {
            "success": True,
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "hostname": parsed.hostname or "",
            "port": parsed.port,
            "path": parsed.path,
            "query": parsed.query,
            "query_params": query_dict,
            "fragment": parsed.fragment
        }
    except Exception as exc:
        return {"success": False, "error": f"URL Parse Error: {str(exc)}"}
