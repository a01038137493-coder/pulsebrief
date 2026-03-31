# -*- coding: utf-8 -*-
"""
Fetches real financial news from NewsAPI.
Returns the same dict schema as mock_news.py so the rest of the pipeline is unchanged.
"""

from datetime import datetime, timedelta, timezone

import requests

import config

_BASE_URL = "https://newsapi.org/v2/top-headlines"


def get_news(hours_back: int = 48) -> list[dict]:
    """
    Fetch recent financial/business headlines from NewsAPI.
    Returns items in the same schema as mock_news.py.
    """
    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours_back)

    response = requests.get(
        _BASE_URL,
        params={
            "category": "business",
            "language": "en",
            "pageSize": 40,
            "apiKey": config.NEWSAPI_KEY,
        },
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "ok":
        raise RuntimeError(f"NewsAPI error: {data.get('message', 'unknown')}")

    items = []
    for article in data.get("articles", []):
        if not article.get("title") or not article.get("source", {}).get("name"):
            continue
        if article["title"].lower() == "[removed]":
            continue

        # Filter by age client-side
        pub = article.get("publishedAt", fetched_at)
        try:
            pub_dt = datetime.fromisoformat(pub.replace("Z", "+00:00"))
            if pub_dt < cutoff:
                continue
        except ValueError:
            pass

        items.append({
            "headline": article["title"],
            "source": article["source"]["name"],
            "published_at": pub,
            "fetched_at": fetched_at,
            "url": article.get("url", ""),
            "body": article.get("description") or article.get("content") or "",
        })

    return items
