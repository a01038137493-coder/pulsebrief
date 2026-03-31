# -*- coding: utf-8 -*-
"""
Combines all news sources and deduplicates by headline similarity.
This is the single entry point the pipeline uses.
"""

from src.ingestion import finnhub, rss


def _headline_key(headline: str) -> str:
    """Rough dedup key — lowercase, strip punctuation, keep first 60 chars."""
    cleaned = "".join(c for c in headline.lower() if c.isalnum() or c == " ")
    return " ".join(cleaned.split())[:60]


def get_all_news() -> list[dict]:
    """Fetch from all sources, deduplicate, sort by published_at desc."""
    all_items = []
    all_items.extend(rss.get_news())
    all_items.extend(finnhub.get_news())

    # Deduplicate by headline key
    seen: set[str] = set()
    unique: list[dict] = []
    for item in all_items:
        key = _headline_key(item["headline"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    # Freshest first
    unique.sort(key=lambda x: x["published_at"], reverse=True)

    print(f"  총 {len(unique)}개 (중복 제거 후)")
    return unique
