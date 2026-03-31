"""
Freshness, credibility, and duplicate filter for news items.

Filters are applied before items reach the LLM summarizer.
Each rejected item gets a 'rejected_reason' for logging/debugging.

Rules:
  - Freshness : published_at must be within MAX_AGE_HOURS of now
  - Credibility: source must be in TRUSTED_SOURCES
  - Duplicates : items sharing 3+ significant keywords with an already-accepted
                 item are dropped (keeps the higher-priority / fresher one)
  - Session    : before sending, briefing must not be older than MAX_BRIEFING_AGE_MINUTES
"""

from datetime import datetime, timezone
from typing import TypedDict


# --- Configuration -----------------------------------------------------------

MAX_AGE_HOURS = 36  # items older than this are too stale for a pre-market brief

TRUSTED_SOURCES = {
    "reuters", "bloomberg", "wsj", "wall street journal",
    "ft", "financial times", "cnbc", "nikkei", "ap",
    "associated press", "barrons", "marketwatch", "the economist",
    "seeking alpha", "axios", "politico",
}

# Words that don't help identify duplicate topics
_STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "to", "of", "for", "and", "or",
    "but", "is", "are", "was", "were", "be", "been", "after", "over",
    "as", "its", "it", "with", "by", "from", "that", "this", "up",
    "down", "new", "says", "say", "said", "report", "reports",
}

DUPLICATE_KEYWORD_THRESHOLD = 3  # shared significant words = likely duplicate

MAX_BRIEFING_AGE_MINUTES = 20  # session freshness re-check threshold


# --- Helpers -----------------------------------------------------------------

def _parse_utc(iso_str: str) -> datetime:
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))


def _hours_ago(iso_str: str) -> float:
    delta = datetime.now(timezone.utc) - _parse_utc(iso_str)
    return delta.total_seconds() / 3600


def _keywords(text: str) -> set[str]:
    words = text.lower().split()
    return {w.strip(".,;:!?\"'()") for w in words if w not in _STOPWORDS and len(w) > 2}


# --- Public API --------------------------------------------------------------

def filter_news(items: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Returns (accepted, rejected).
    Accepted items have a 'freshness_hours' field added.
    Rejected items have a 'rejected_reason' field added.
    """
    accepted: list[dict] = []
    rejected: list[dict] = []
    seen_keywords: set[str] = set()

    # Sort freshest first so duplicates keep the most recent item
    sorted_items = sorted(items, key=lambda x: x["published_at"], reverse=True)

    for item in sorted_items:
        item = dict(item)  # don't mutate the original

        # 1. Freshness check
        hours_old = _hours_ago(item["published_at"])
        item["freshness_hours"] = round(hours_old, 1)
        if hours_old > MAX_AGE_HOURS:
            item["rejected_reason"] = f"stale ({hours_old:.1f}h old, limit {MAX_AGE_HOURS}h)"
            rejected.append(item)
            continue

        # 2. Credibility check
        source_lower = item["source"].lower()
        if not any(trusted in source_lower for trusted in TRUSTED_SOURCES):
            item["rejected_reason"] = f"untrusted source ({item['source']!r})"
            rejected.append(item)
            continue

        # 3. Duplicate check
        keywords = _keywords(item["headline"])
        overlap = keywords & seen_keywords
        if len(overlap) >= DUPLICATE_KEYWORD_THRESHOLD:
            item["rejected_reason"] = f"duplicate (overlapping keywords: {overlap})"
            rejected.append(item)
            continue

        seen_keywords |= keywords
        accepted.append(item)

    return accepted, rejected


def is_briefing_fresh(generated_at: datetime) -> bool:
    """
    Re-checks whether a briefing is still fresh enough to send.
    Call this immediately before Telegram delivery.
    """
    age_minutes = (datetime.now(timezone.utc) - generated_at).total_seconds() / 60
    return age_minutes <= MAX_BRIEFING_AGE_MINUTES
