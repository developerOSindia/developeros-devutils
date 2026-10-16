"""
Cron Builder & Schedule Explainer Core Module.
Pure Python, standard-library implementation with zero external dependencies.
"""

from typing import Dict, Any, List

DOW_MAP = {
    "0": "Sunday", "1": "Monday", "2": "Tuesday", "3": "Wednesday",
    "4": "Thursday", "5": "Friday", "6": "Saturday", "7": "Sunday"
}

MONTH_MAP = {
    "1": "January", "2": "February", "3": "March", "4": "April",
    "5": "May", "6": "June", "7": "July", "8": "August",
    "9": "September", "10": "October", "11": "November", "12": "December"
}

PRESETS = {
    "Every Minute": "* * * * *",
    "Every 5 Minutes": "*/5 * * * *",
    "Every 15 Minutes": "*/15 * * * *",
    "Every Hour at :00": "0 * * * *",
    "Every Day at Midnight (00:00)": "0 0 * * *",
    "Every Day at Noon (12:00)": "0 12 * * *",
    "Every Sunday at Midnight": "0 0 * * 0",
    "Every 1st of the Month at 00:00": "0 0 1 * *",
}


def explain_cron(expression: str) -> Dict[str, Any]:
    """Parses and explains a 5-part cron expression in plain English."""
    if not expression or not expression.strip():
        return {"success": False, "error": "Cron expression cannot be empty."}

    parts = expression.strip().split()
    if len(parts) != 5:
        return {
            "success": False,
            "error": f"Invalid cron expression: Expected 5 fields (min hour dom mon dow), received {len(parts)}."
        }

    minute, hour, dom, month, dow = parts

    desc_parts: List[str] = []

    # Minute
    if minute == "*":
        desc_parts.append("every minute")
    elif minute.startswith("*/"):
        desc_parts.append(f"every {minute[2:]} minutes")
    else:
        desc_parts.append(f"at minute {minute}")

    # Hour
    if hour == "*":
        desc_parts.append("of every hour")
    elif hour.startswith("*/"):
        desc_parts.append(f"every {hour[2:]} hours")
    else:
        desc_parts.append(f"past hour {hour}:00")

    # Day of Month
    if dom != "*":
        if dom.startswith("*/"):
            desc_parts.append(f"every {dom[2:]} days")
        else:
            desc_parts.append(f"on day {dom} of the month")

    # Month
    if month != "*":
        m_name = MONTH_MAP.get(month, f"month {month}")
        desc_parts.append(f"in {m_name}")

    # Day of Week
    if dow != "*":
        dow_name = DOW_MAP.get(dow, f"day-of-week {dow}")
        desc_parts.append(f"on {dow_name}")

    human_description = "Runs " + ", ".join(desc_parts) + "."

    return {
        "success": True,
        "expression": expression.strip(),
        "fields": {
            "minute": minute,
            "hour": hour,
            "day_of_month": dom,
            "month": month,
            "day_of_week": dow
        },
        "description": human_description
    }


def build_cron(
    minute: str = "*",
    hour: str = "*",
    dom: str = "*",
    month: str = "*",
    dow: str = "*"
) -> str:
    """Combines 5 fields into a valid cron expression."""
    return f"{minute.strip()} {hour.strip()} {dom.strip()} {month.strip()} {dow.strip()}"
