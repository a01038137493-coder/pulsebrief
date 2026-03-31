"""
User preferences — stored as a single JSON file.
No database for MVP. Easy to swap in later.
"""

import json
from pathlib import Path

_PREFS_PATH = Path(__file__).parent.parent.parent / "data" / "preferences.json"

DEFAULTS: dict = {
    "watchlist": [],
    "sectors": [],
    "target_market": "US Equities",
    "interval_minutes": 10,
    "active_hour_start": "04:00",
    "active_hour_end": "10:00",
    "briefing_detail": "normal",       # short | normal | detailed
    "briefing_items": 5,               # 3 | 5 | 7 | 10
    "news_sources": ["reuters", "cnbc", "marketwatch", "finnhub"],
    "language": "ko",                  # ko | en
    "urgent_alerts": False,
    "alert_market_open": False,
    "alert_market_close": False,
    "dedup_filter": True,
    "max_age_hours": 36,               # 6 | 12 | 24 | 36
}


def load() -> dict:
    if not _PREFS_PATH.exists():
        return dict(DEFAULTS)
    with open(_PREFS_PATH, encoding="utf-8") as f:
        saved = json.load(f)
    return {**DEFAULTS, **saved}


def save(prefs: dict) -> None:
    _PREFS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)
