"""
User preferences — per-user JSON files under data/users/.
Registry at data/users/registry.json.

Legacy single-user API (load/save) kept for web UI backward compat.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

_DATA_DIR = Path(__file__).parent.parent.parent / "data"
_USERS_DIR = _DATA_DIR / "users"
_REGISTRY_PATH = _USERS_DIR / "registry.json"
_LEGACY_PREFS_PATH = _DATA_DIR / "preferences.json"

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


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

def _load_registry() -> dict:
    if not _REGISTRY_PATH.exists():
        return {}
    with open(_REGISTRY_PATH, encoding="utf-8") as f:
        return json.load(f)


def _save_registry(registry: dict) -> None:
    _USERS_DIR.mkdir(parents=True, exist_ok=True)
    with open(_REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def list_users() -> list[str]:
    """Return list of registered chat_ids."""
    return list(_load_registry().keys())


def register_user(chat_id: str) -> bool:
    """Register new user with default prefs.

    Returns True if this is a new user, False if already registered.
    """
    registry = _load_registry()
    if chat_id in registry:
        return False
    registry[chat_id] = {"registered_at": datetime.now(timezone.utc).isoformat()}
    _save_registry(registry)
    # Initialize preferences file only if it doesn't exist yet
    prefs_path = _USERS_DIR / f"{chat_id}.json"
    if not prefs_path.exists():
        save_user(chat_id, dict(DEFAULTS))
    return True


def unregister_user(chat_id: str) -> None:
    """Remove user from registry (preferences file is kept for potential re-registration)."""
    registry = _load_registry()
    registry.pop(chat_id, None)
    _save_registry(registry)


# ---------------------------------------------------------------------------
# Per-user preferences
# ---------------------------------------------------------------------------

def load_user(chat_id: str) -> dict:
    path = _USERS_DIR / f"{chat_id}.json"
    if not path.exists():
        return dict(DEFAULTS)
    with open(path, encoding="utf-8") as f:
        saved = json.load(f)
    return {**DEFAULTS, **saved}


def save_user(chat_id: str, user_prefs: dict) -> None:
    _USERS_DIR.mkdir(parents=True, exist_ok=True)
    path = _USERS_DIR / f"{chat_id}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(user_prefs, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Legacy single-user API — used by web UI (/save endpoint)
# ---------------------------------------------------------------------------

def load() -> dict:
    if _LEGACY_PREFS_PATH.exists():
        with open(_LEGACY_PREFS_PATH, encoding="utf-8") as f:
            saved = json.load(f)
        return {**DEFAULTS, **saved}
    return dict(DEFAULTS)


def save(user_prefs: dict) -> None:
    _LEGACY_PREFS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(_LEGACY_PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(user_prefs, f, ensure_ascii=False, indent=2)
