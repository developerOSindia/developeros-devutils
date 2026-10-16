"""
JWT Decoder Core Module.
Pure Python, standard-library implementation with zero external dependencies.
Decodes JSON Web Tokens into Header and Payload.
NOTE: This is client-side structural decoding, NOT cryptographic verification.
"""

import base64
import datetime
import json
from typing import Dict, Any

SECURITY_DISCLAIMER = (
    "SECURITY NOTICE: This token was structurally decoded client-side. "
    "The cryptographic signature HAS NOT been verified against a secret or public key. "
    "Do not trust claims from unverified tokens for sensitive access decisions."
)


def _base64url_decode(segment: str) -> bytes:
    """Decodes standard base64url segment."""
    rem = len(segment) % 4
    if rem > 0:
        segment += "=" * (4 - rem)
    return base64.urlsafe_b64decode(segment.encode("ascii"))


def decode_jwt(token_str: str) -> Dict[str, Any]:
    """Decodes a 3-part JSON Web Token without cryptographic verification."""
    if not token_str or not token_str.strip():
        return {"success": False, "error": "Token string is empty."}

    parts = token_str.strip().split(".")
    if len(parts) != 3:
        return {
            "success": False,
            "error": f"Invalid JWT structure: Expected 3 period-separated parts (header.payload.signature), received {len(parts)}."
        }

    header_b64, payload_b64, signature_b64 = parts

    try:
        header_json = _base64url_decode(header_b64).decode("utf-8")
        header = json.loads(header_json)
    except Exception as exc:
        return {"success": False, "error": f"Failed to decode JWT Header: {str(exc)}"}

    try:
        payload_json = _base64url_decode(payload_b64).decode("utf-8")
        payload = json.loads(payload_json)
    except Exception as exc:
        return {"success": False, "error": f"Failed to decode JWT Payload: {str(exc)}"}

    # Human-readable timestamps
    claims_info = {}
    time_keys = ["exp", "iat", "nbf"]
    for tk in time_keys:
        if tk in payload and isinstance(payload[tk], (int, float)):
            try:
                dt = datetime.datetime.fromtimestamp(payload[tk], tz=datetime.timezone.utc)
                claims_info[f"{tk}_formatted"] = dt.strftime("%Y-%m-%d %H:%M:%S UTC")
                if tk == "exp":
                    now = datetime.datetime.now(datetime.timezone.utc)
                    claims_info["is_expired"] = now > dt
            except Exception:
                pass

    return {
        "success": True,
        "header": header,
        "payload": payload,
        "signature_raw": signature_b64,
        "claims_info": claims_info,
        "security_disclaimer": SECURITY_DISCLAIMER
    }
