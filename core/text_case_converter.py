"""
Text Case Converter Core Module.
Pure Python, standard-library implementation with zero external dependencies.
Splits strings cleanly across camelCase, snake_case, kebab-case, spaces, and punctuation,
and converts to any programming casing convention.
"""

import re
from typing import Dict, Any, List

MAX_TEXT_LEN = 500000


def _split_into_words(text: str) -> List[str]:
    """Splits arbitrary text by spaces, punctuation, underscores, dashes, and camelCase transitions."""
    # Insert boundary space before uppercase followed by lowercase (e.g. camelCase -> camel Case)
    s1 = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    # Insert boundary space between consecutive capitals and lowercase (e.g. JSONParser -> JSON Parser)
    s2 = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s1)
    # Split on non-alphanumeric characters
    words = re.findall(r"[A-Za-z0-9]+", s2)
    return words


def convert_cases(text: str) -> Dict[str, Any]:
    """Converts input text into all standard casing conventions."""
    if text is None:
        return {"success": False, "error": "Text cannot be None."}

    if len(text) > MAX_TEXT_LEN:
        return {"success": False, "error": f"Input exceeds maximum limit of {MAX_TEXT_LEN} characters."}

    if not text.strip():
        return {
            "success": True,
            "lowercase": "",
            "uppercase": "",
            "title_case": "",
            "sentence_case": "",
            "camel_case": "",
            "pascal_case": "",
            "snake_case": "",
            "constant_case": "",
            "kebab_case": "",
            "cobol_case": "",
            "dot_case": "",
            "path_case": ""
        }

    words = _split_into_words(text)
    lower_words = [w.lower() for w in words]
    cap_words = [w.capitalize() for w in words]

    # Casing transformations
    lower_str = " ".join(lower_words)
    upper_str = " ".join([w.upper() for w in words])
    title_str = " ".join(cap_words)

    # Sentence case
    sentence_str = (lower_words[0].capitalize() + " " + " ".join(lower_words[1:])).strip() if lower_words else ""

    # CamelCase: first word lower, subsequent capitalized
    camel_str = (lower_words[0] + "".join(cap_words[1:])) if lower_words else ""

    # PascalCase: all words capitalized
    pascal_str = "".join(cap_words)

    # snake_case: joined with underscore
    snake_str = "_".join(lower_words)

    # CONSTANT_CASE: uppercase joined with underscore
    constant_str = "_".join([w.upper() for w in words])

    # kebab-case: joined with hyphen
    kebab_str = "-".join(lower_words)

    # COBOL-CASE: uppercase joined with hyphen
    cobol_str = "-".join([w.upper() for w in words])

    # dot.case: joined with dot
    dot_str = ".".join(lower_words)

    # path/case: joined with forward slash
    path_str = "/".join(lower_words)

    return {
        "success": True,
        "lowercase": lower_str,
        "uppercase": upper_str,
        "title_case": title_str,
        "sentence_case": sentence_str,
        "camel_case": camel_str,
        "pascal_case": pascal_str,
        "snake_case": snake_str,
        "constant_case": constant_str,
        "kebab_case": kebab_str,
        "cobol_case": cobol_str,
        "dot_case": dot_str,
        "path_case": path_str
    }
