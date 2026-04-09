"""
utils.py — Helper utilities for Artisia AI output formatting.
"""

import json


def format_readiness_score(score: int) -> str:
    """Return a human-readable label for a Global Readiness Score."""
    if score >= 90:
        return "🏆 Exceptional — Enterprise Ready"
    elif score >= 75:
        return "✅ Strong — Ready to Launch"
    elif score >= 60:
        return "⚡ Good — Minor Improvements Needed"
    elif score >= 40:
        return "⚠️ Fair — Significant Gaps Present"
    else:
        return "🔴 Weak — Major Revision Required"


def format_json_output(result: dict) -> str:
    """Return a pretty-printed JSON string of the full pipeline result."""
    return json.dumps(result, indent=2, ensure_ascii=False)


def clean_text(text: str) -> str:
    """Strip extra whitespace and normalize line breaks."""
    if not text:
        return ""
    return " ".join(text.split())


def format_price_range(price_range: dict) -> str:
    """Format a price range dict into a readable string."""
    if not price_range:
        return "—"
    currency = price_range.get("currency", "USD")
    low = price_range.get("low", 0)
    high = price_range.get("high", 0)
    return f"${low:,.0f} – ${high:,.0f} {currency}"


def truncate(text: str, max_chars: int = 200) -> str:
    """Truncate a string to max_chars with ellipsis."""
    if not text or len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + "…"


def bullet_list(items: list) -> str:
    """Convert a list to a markdown bullet list string."""
    if not items:
        return "—"
    return "\n".join(f"• {item}" for item in items)


def safe_get(d: dict, *keys, default=None):
    """Safely traverse nested dicts with multiple keys."""
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, default)
    return d
