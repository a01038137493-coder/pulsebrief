"""
User preferences — stored as a single JSON file.
No database for MVP. Easy to swap in later.

Schema:
  watchlist        : list of ticker symbols  e.g. ["NVDA", "AAPL"]
  sectors          : list of sector names    e.g. ["semiconductors", "energy"]
  target_market    : str                     e.g. "US Equities"
  interval_minutes : int                     e.g. 10, 20, 30, 60
  urgent_alerts    : bool
"""

import json
from pathlib import Path

_PREFS_PATH = Path(__file__).parent.parent.parent / "data" / "preferences.json"

DEFAULTS: dict = {
    "watchlist": [],
    "sectors": [],
    "target_market": "US Equities",
    "interval_minutes": 10,
    "urgent_alerts": False,
}


def load() -> dict:
    if not _PREFS_PATH.exists():
        return dict(DEFAULTS)
    with open(_PREFS_PATH, encoding="utf-8") as f:
        saved = json.load(f)
    # Fill in any missing keys with defaults
    return {**DEFAULTS, **saved}


def save(prefs: dict) -> None:
    _PREFS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)
