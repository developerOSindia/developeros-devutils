"""
Color Converter Core Module.
Pure Python, standard-library implementation with zero external dependencies.
Supports bidirectional conversion between HEX, RGB, HSL, and CMYK, plus WCAG contrast calculation.
"""

import colorsys
import re
from typing import Dict, Any, Tuple


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Parses a hex color string into (R, G, B) tuple 0-255."""
    clean = hex_str.strip().lstrip("#")
    if len(clean) == 3:
        clean = "".join([c * 2 for c in clean])
    if len(clean) != 6:
        raise ValueError(f"Invalid HEX color: #{hex_str}")
    return int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Formats (R, G, B) into #RRGGBB."""
    return f"#{r:02x}{g:02x}{b:02x}".lower()


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """Converts (R, G, B) [0-255] to (H [0-360], S [0-100], L [0-100])."""
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
    return round(h * 360), round(s * 100), round(l * 100)


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    """Converts (H [0-360], S [0-100], L [0-100]) to (R, G, B) [0-255]."""
    h_norm = (h % 360) / 360.0
    s_norm = max(0.0, min(1.0, s / 100.0))
    l_norm = max(0.0, min(1.0, l / 100.0))
    r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)
    return round(r * 255), round(g * 255), round(b * 255)


def rgb_to_cmyk(r: int, g: int, b: int) -> Tuple[int, int, int, int]:
    """Converts (R, G, B) [0-255] to (C, M, Y, K) [0-100%]."""
    if r == 0 and g == 0 and b == 0:
        return 0, 0, 0, 100
    r_norm, g_norm, b_norm = r / 255.0, g / 255.0, b / 255.0
    k = 1.0 - max(r_norm, g_norm, b_norm)
    c = (1.0 - r_norm - k) / (1.0 - k)
    m = (1.0 - g_norm - k) / (1.0 - k)
    y = (1.0 - b_norm - k) / (1.0 - k)
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)


def calculate_relative_luminance(r: int, g: int, b: int) -> float:
    """Calculates relative luminance according to WCAG 2.1 specs."""
    def _srgb_to_linear(val: float) -> float:
        val = val / 255.0
        return val / 12.92 if val <= 0.03928 else ((val + 0.055) / 1.055) ** 2.4

    r_lin = _srgb_to_linear(r)
    g_lin = _srgb_to_linear(g)
    b_lin = _srgb_to_linear(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def calculate_contrast_ratio(lum1: float, lum2: float) -> float:
    """Calculates contrast ratio between two relative luminances."""
    bright = max(lum1, lum2)
    dark = min(lum1, lum2)
    return round((bright + 0.05) / (dark + 0.05), 2)


def convert_color(color_input: str) -> Dict[str, Any]:
    """Auto-detects and converts any standard color format into all representation formats."""
    if not color_input or not color_input.strip():
        return {"success": False, "error": "Color input cannot be empty."}

    val = color_input.strip().lower()

    try:
        if val.startswith("#") or (len(val) in (3, 6) and all(c in "0123456789abcdef" for c in val)):
            # HEX
            r, g, b = hex_to_rgb(val)
        elif val.startswith("rgb"):
            nums = [int(n.strip()) for n in re.findall(r"\d+", val)[:3]]
            if len(nums) != 3:
                raise ValueError("Expected 3 RGB integer values.")
            r, g, b = nums
        elif val.startswith("hsl"):
            nums = [int(n.strip()) for n in re.findall(r"\d+", val)[:3]]
            if len(nums) != 3:
                raise ValueError("Expected 3 HSL integer values (h, s, l).")
            r, g, b = hsl_to_rgb(nums[0], nums[1], nums[2])
        else:
            # Fallback to hex parsing
            r, g, b = hex_to_rgb(val)

        # Validate RGB range
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))

        hex_code = rgb_to_hex(r, g, b)
        h, s, l = rgb_to_hsl(r, g, b)
        c, m, y, k = rgb_to_cmyk(r, g, b)

        lum = calculate_relative_luminance(r, g, b)
        contrast_white = calculate_contrast_ratio(lum, 1.0)
        contrast_black = calculate_contrast_ratio(lum, 0.0)

        return {
            "success": True,
            "hex": hex_code,
            "rgb": f"rgb({r}, {g}, {b})",
            "rgb_tuple": (r, g, b),
            "hsl": f"hsl({h}, {s}%, {l}%)",
            "hsl_tuple": (h, s, l),
            "cmyk": f"cmyk({c}%, {m}%, {y}%, {k}%)",
            "cmyk_tuple": (c, m, y, k),
            "relative_luminance": round(lum, 4),
            "contrast_on_white": contrast_white,
            "contrast_on_black": contrast_black,
            "wcag_aa_white": contrast_white >= 4.5,
            "wcag_aa_black": contrast_black >= 4.5
        }
    except Exception as exc:
        return {"success": False, "error": f"Color Parsing Error: {str(exc)}"}
