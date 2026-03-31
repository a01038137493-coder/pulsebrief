# -*- coding: utf-8 -*-
"""
Fetches real-time market news from Finnhub.
Requires FINNHUB_KEY in .env. Skipped silently if key is not set.

Free tier: 60 calls/min, real-time news included.
Get key at: https://finnhub.io
"""

import os
from datetime import datetime, timezone

import requests


def get_news() -> list[dict]:
    key = os.environ.get("FINNHUB_KEY", "")
    if not key:
        print("  [Finnhub] 키 없음 — 건너뜀 (FINNHUB_KEY를 .env에 추가)")
        return []

    fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    items = []

    try:
        response = requests.get(
            "https://finnhub.io/api/v1/news",
            params={"category": "general", "token": key},
            timeout=10,
        )
        response.raise_for_status()
        articles = response.json()

        for article in articles[:30]:
            ts = article.get("datetime", 0)
            published_at = (
                datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                if ts else fetched_at
            )
            headline = article.get("headline", "").strip()
            if not headline:
                continue
            items.append({
                "headline": headline,
                "source": article.get("source", "Finnhub"),
                "published_at": published_at,
                "fetched_at": fetched_at,
                "url": article.get("url", ""),
                "body": article.get("summary", ""),
            })

        print(f"  [Finnhub] {len(items)}개 수집")

    except Exception as e:
        print(f"  [Finnhub] 실패: {e}")

    return items
