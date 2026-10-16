"""
Unix Timestamp Converter Core Module.
Pure Python, standard-library implementation using datetime and time.
"""

import datetime
import time
from typing import Dict, Any


def timestamp_to_datetimes(ts_val: float | int, is_millis: bool = False) -> Dict[str, Any]:
    """Converts a Unix timestamp (seconds or millis) into various datetime formats."""
    try:
        raw_seconds = float(ts_val)
        if is_millis or raw_seconds > 1e11:  # Timestamp likely in milliseconds
            seconds = raw_seconds / 1000.0
            millis = int(raw_seconds)
        else:
            seconds = raw_seconds
            millis = int(raw_seconds * 1000)

        dt_utc = datetime.datetime.fromtimestamp(seconds, tz=datetime.timezone.utc)
        dt_local = dt_utc.astimezone()

        now_utc = datetime.datetime.now(datetime.timezone.utc)
        diff_seconds = (now_utc - dt_utc).total_seconds()

        # Relative time description
        if abs(diff_seconds) < 60:
            relative = "just now"
        elif diff_seconds > 0:
            if diff_seconds < 3600:
                relative = f"{int(diff_seconds // 60)} minutes ago"
            elif diff_seconds < 86400:
                relative = f"{int(diff_seconds // 3600)} hours ago"
            else:
                relative = f"{int(diff_seconds // 86400)} days ago"
        else:
            fut = abs(diff_seconds)
            if fut < 3600:
                relative = f"in {int(fut // 60)} minutes"
            elif fut < 86400:
                relative = f"in {int(fut // 3600)} hours"
            else:
                relative = f"in {int(fut // 86400)} days"

        return {
            "success": True,
            "seconds": int(seconds),
            "milliseconds": millis,
            "iso_8601": dt_utc.isoformat(),
            "utc_string": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "local_string": dt_local.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "rfc_2822": dt_utc.strftime("%a, %d %b %Y %H:%M:%S +0000"),
            "relative": relative
        }
    except Exception as exc:
        return {"success": False, "error": f"Invalid Timestamp: {str(exc)}"}


def datetime_to_timestamp(dt_str: str) -> Dict[str, Any]:
    """Parses standard ISO 8601 or YYYY-MM-DD HH:MM:SS string to Unix timestamp."""
    if not dt_str or not dt_str.strip():
        return {"success": False, "error": "Datetime string cannot be empty."}

    clean_str = dt_str.strip()
    parsed_dt = None

    # Try common formats
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S%z",
    ]

    for fmt in formats:
        try:
            parsed_dt = datetime.datetime.strptime(clean_str, fmt)
            break
        except ValueError:
            continue

    if parsed_dt is None:
        try:
            parsed_dt = datetime.datetime.fromisoformat(clean_str)
        except Exception:
            pass

    if parsed_dt is None:
        return {
            "success": False,
            "error": "Could not parse datetime string. Use ISO 8601 or 'YYYY-MM-DD HH:MM:SS'."
        }

    if parsed_dt.tzinfo is None:
        parsed_dt = parsed_dt.replace(tzinfo=datetime.timezone.utc)

    epoch_seconds = int(parsed_dt.timestamp())
    epoch_millis = int(parsed_dt.timestamp() * 1000)

    return {
        "success": True,
        "seconds": epoch_seconds,
        "milliseconds": epoch_millis,
        "iso_8601": parsed_dt.isoformat()
    }


def get_current_timestamp() -> Dict[str, Any]:
    """Returns current system timestamp in seconds and milliseconds."""
    now = time.time()
    return {
        "seconds": int(now),
        "milliseconds": int(now * 1000),
        "iso_8601": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
