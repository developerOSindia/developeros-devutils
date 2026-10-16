"""
Markdown Previewer & Analyzer Core Module.
Pure Python, standard-library implementation with zero external dependencies.
"""

import re
from typing import Dict, Any, List

MAX_MD_LEN = 200000


def analyze_markdown(markdown_text: str) -> Dict[str, Any]:
    """Analyzes markdown document structure, headings, links, and code blocks."""
    if markdown_text is None:
        return {"success": False, "error": "Markdown text cannot be None."}

    if len(markdown_text) > MAX_MD_LEN:
        return {"success": False, "error": f"Markdown exceeds maximum limit of {MAX_MD_LEN} characters."}

    # Extract headings for Table of Contents
    heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
    headings: List[Dict[str, Any]] = []
    for m in heading_pattern.finditer(markdown_text):
        level = len(m.group(1))
        title = m.group(2).strip()
        headings.append({"level": level, "title": title})

    # Count links [text](url) - ignore images ![alt](url)
    link_pattern = re.compile(r"(?<!\!)\[([^\]]+)\]\(([^)]+)\)")
    links = link_pattern.findall(markdown_text)

    # Count images ![alt](url)
    image_pattern = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
    images = image_pattern.findall(markdown_text)

    # Count code blocks ```...```
    code_block_pattern = re.compile(r"```[a-zA-Z0-9_-]*\n[\s\S]*?```")
    code_blocks = code_block_pattern.findall(markdown_text)

    # Word count
    words = re.findall(r"\b\w+\b", markdown_text)
    word_count = len(words)
    read_time_mins = max(1, round(word_count / 200.0, 1))

    # Detect potentially unsafe HTML tags (XSS check)
    unsafe_tags = re.findall(r"<\s*(script|iframe|object|embed|applet|style)\b[^>]*>", markdown_text, re.IGNORECASE)
    has_unsafe_html = len(unsafe_tags) > 0

    return {
        "success": True,
        "char_count": len(markdown_text),
        "word_count": word_count,
        "estimated_reading_minutes": read_time_mins,
        "headings_count": len(headings),
        "headings": headings,
        "links_count": len(links),
        "images_count": len(images),
        "code_blocks_count": len(code_blocks),
        "has_unsafe_html": has_unsafe_html,
        "unsafe_tags_found": list(set(unsafe_tags)) if has_unsafe_html else []
    }
