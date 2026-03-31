# -*- coding: utf-8 -*-
"""
Fetches real-time financial news from public RSS feeds.
No API key required.
"""

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser

FEEDS = [
    ("Reuters Business", "https://feeds.reuters.com/reuters/businessNews"),
    ("CNBC", "https://www.cnbc.com/id/100003114/device/rss/rss.html"),
    ("MarketWatch", "https://feeds.marketwatch.com/marketwatch/topstories/"),
]


def _parse_date(entry) -> str:
    """Parse RSS date to ISO 8601 UTC string."""
    for field in ("published", "updated"):
        val = getattr(entry, field, None)
        if val:
            try:
                dt = parsedate_to_datetime(val)
                return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            except Exception:
                pass
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_news() -> list[dict]:
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    items = []

    for source_name, url in FEEDS:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:15]:
                title = getattr(entry, "title", "").strip()
                if not title:
                    continue
                items.append({
                    "headline": title,
                    "source": source_name,
                    "published_at": _parse_date(entry),
                    "fetched_at": fetched_at,
                    "url": getattr(entry, "link", ""),
                    "body": getattr(entry, "summary", "") or getattr(entry, "description", ""),
                })
        except Exception as e:
            print(f"  [RSS] {source_name} 실패: {e}")

    print(f"  [RSS] {len(items)}개 수집")
    return items
