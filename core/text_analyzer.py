"""
Text Analyzer & Metrics Core Module.
Pure Python, standard-library implementation with zero external dependencies.
"""

import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Any, List

MAX_TEXT_BYTES = 1024 * 1024  # 1 MB Limit


@dataclass(frozen=True)
class TextMetrics:
    total_chars: int
    chars_no_spaces: int
    total_words: int
    total_lines: int
    total_sentences: int
    reading_time_sec: float
    shannon_entropy: float
    top_words: List[tuple[str, int]]
    success: bool
    error: str | None = None


def calculate_entropy(text: str) -> float:
    """Calculates Shannon entropy in bits per character."""
    if not text:
        return 0.0
    length = len(text)
    counts = Counter(text)
    entropy = 0.0
    for count in counts.values():
        prob = count / length
        entropy -= prob * math.log2(prob)
    return round(entropy, 4)


def analyze_text(text: str) -> TextMetrics:
    """Analyzes text properties, frequency, and readability metrics."""
    if text is None:
        return TextMetrics(0, 0, 0, 0, 0, 0.0, 0.0, [], False, "Input cannot be None.")

    byte_len = len(text.encode("utf-8", errors="ignore"))
    if byte_len > MAX_TEXT_BYTES:
        return TextMetrics(
            0, 0, 0, 0, 0, 0.0, 0.0, [], False,
            f"Input exceeds maximum allowed size of 1 MB ({byte_len} bytes)."
        )

    if not text.strip():
        return TextMetrics(
            total_chars=len(text),
            chars_no_spaces=0,
            total_words=0,
            total_lines=len(text.splitlines()) or (1 if text else 0),
            total_sentences=0,
            reading_time_sec=0.0,
            shannon_entropy=0.0,
            top_words=[],
            success=True,
        )

    chars_total = len(text)
    chars_no_space = len(re.sub(r"\s+", "", text))
    words = re.findall(r"\b\w+\b", text.lower())
    total_words = len(words)
    lines = len(text.splitlines()) or 1
    sentences = len(re.findall(r"[.!?]+", text)) or (1 if words else 0)

    # 200 words per minute average reading speed
    reading_time_sec = round((total_words / 200.0) * 60, 1)
    entropy = calculate_entropy(text)

    # Top words excluding short words
    meaningful_words = [w for w in words if len(w) > 2]
    top_words = Counter(meaningful_words).most_common(5)

    return TextMetrics(
        total_chars=chars_total,
        chars_no_spaces=chars_no_space,
        total_words=total_words,
        total_lines=lines,
        total_sentences=sentences,
        reading_time_sec=reading_time_sec,
        shannon_entropy=entropy,
        top_words=top_words,
        success=True,
    )


def transform_text_case(text: str, mode: str) -> Dict[str, Any]:
    """Applies case transformation to input text."""
    if len(text.encode("utf-8", errors="ignore")) > MAX_TEXT_BYTES:
        return {"output": "", "success": False, "error": "Input exceeds 1 MB limit."}

    mode = mode.lower()
    if mode == "upper":
        res = text.upper()
    elif mode == "lower":
        res = text.lower()
    elif mode == "title":
        res = text.title()
    elif mode == "snake":
        res = re.sub(r"[\s\-]+", "_", text.strip()).lower()
    elif mode == "kebab":
        res = re.sub(r"[\s_]+", "-", text.strip()).lower()
    elif mode == "camel":
        words = re.split(r"[\s_\-]+", text.strip())
        res = words[0].lower() + "".join(w.capitalize() for w in words[1:]) if words else ""
    else:
        res = text

    return {"output": res, "success": True, "mode": mode}
