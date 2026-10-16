"""
Hash & HMAC Generator Core Module.
Pure Python, standard-library implementation using hashlib and hmac.
"""

import hashlib
import hmac
from typing import Dict, Any, List

SUPPORTED_ALGORITHMS = ["sha256", "sha512", "sha1", "md5", "sha384", "sha224"]
MAX_INPUT_BYTES = 1024 * 1024  # 1 MB Limit


def generate_hashes(text: str) -> Dict[str, Any]:
    """Generates standard hashes for input text."""
    if text is None:
        return {"hashes": {}, "success": False, "error": "Input cannot be None."}

    data = text.encode("utf-8")
    if len(data) > MAX_INPUT_BYTES:
        return {
            "hashes": {},
            "success": False,
            "error": f"Input exceeds 1 MB limit ({len(data)} bytes)."
        }

    hashes = {}
    for algo in SUPPORTED_ALGORITHMS:
        h = hashlib.new(algo)
        h.update(data)
        hashes[algo.upper()] = h.hexdigest()

    return {
        "hashes": hashes,
        "input_length": len(text),
        "input_bytes": len(data),
        "success": True
    }


def generate_hmac(text: str, secret_key: str, algorithm: str = "sha256") -> Dict[str, Any]:
    """Computes Hash-based Message Authentication Code (HMAC)."""
    if text is None or secret_key is None:
        return {"hmac": "", "success": False, "error": "Text and secret key cannot be None."}

    algo = algorithm.lower()
    if algo not in SUPPORTED_ALGORITHMS:
        return {"hmac": "", "success": False, "error": f"Unsupported algorithm: {algorithm}"}

    data = text.encode("utf-8")
    key = secret_key.encode("utf-8")

    if len(data) > MAX_INPUT_BYTES:
        return {"hmac": "", "success": False, "error": "Input text exceeds 1 MB limit."}

    digest = hmac.new(key, data, getattr(hashlib, algo)).hexdigest()
    return {
        "hmac": digest,
        "algorithm": algo.upper(),
        "success": True
    }


def verify_hash(candidate: str, expected_hash: str) -> bool:
    """Constant-time hash comparison to prevent timing attacks."""
    if not candidate or not expected_hash:
        return False
    return hmac.compare_digest(candidate.strip().lower(), expected_hash.strip().lower())
