"""
Mock news items for MVP pipeline testing.
Each dict represents the contract that real ingestion will later satisfy.

Required fields per item:
  headline    : str
  source      : str
  published_at: ISO 8601 UTC string
  fetched_at  : ISO 8601 UTC string  (when our system retrieved it)
  url         : str
  body        : str
"""

from datetime import datetime, timezone


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get_mock_news() -> list[dict]:
    fetched = _now()
    return [
        {
            "headline": "Fed's Waller signals no rate cuts until inflation shows more progress",
            "source": "Reuters",
            "published_at": "2026-04-01T06:15:00Z",
            "fetched_at": fetched,
            "url": "https://www.reuters.com/mock/waller-rate-cuts",
            "body": (
                "Federal Reserve Governor Christopher Waller said Monday he needs to see "
                "several more months of favorable inflation data before supporting rate cuts. "
                "His comments pushed 2-year Treasury yields higher in overnight trading."
            ),
        },
        {
            "headline": "NVIDIA surges 6% in after-hours after blowout Q1 guidance raise",
            "source": "Bloomberg",
            "published_at": "2026-04-01T05:45:00Z",
            "fetched_at": fetched,
            "url": "https://www.bloomberg.com/mock/nvidia-guidance",
            "body": (
                "NVIDIA raised its Q1 revenue guidance to $43B, well above the $38.5B consensus. "
                "The company cited continued hyperscaler demand for Blackwell GPUs. "
                "Shares jumped 6% in extended trading, dragging semis broadly higher."
            ),
        },
        {
            "headline": "Oil rises 2% after Saudi Arabia announces surprise production cut",
            "source": "FT",
            "published_at": "2026-04-01T04:30:00Z",
            "fetched_at": fetched,
            "url": "https://www.ft.com/mock/saudi-cut",
            "body": (
                "Saudi Arabia said it would cut output by 500,000 bpd starting in May, "
                "citing market stabilization goals. WTI crude rose to $84.20. "
                "Energy names and inflation-linked assets moved higher overnight."
            ),
        },
        {
            "headline": "China PMI beats expectations, lifting Asia markets",
            "source": "WSJ",
            "published_at": "2026-04-01T03:00:00Z",
            "fetched_at": fetched,
            "url": "https://www.wsj.com/mock/china-pmi",
            "body": (
                "China's official manufacturing PMI came in at 51.2 for March, above the 50.5 estimate. "
                "Hang Seng rose 1.4%, and copper futures moved higher on improved demand outlook. "
                "Metals and mining names may see follow-through at US open."
            ),
        },
        {
            "headline": "Apple supplier Foxconn reports record quarterly revenue",
            "source": "Nikkei",
            "published_at": "2026-04-01T02:15:00Z",
            "fetched_at": fetched,
            "url": "https://asia.nikkei.com/mock/foxconn-revenue",
            "body": (
                "Foxconn reported Q1 revenue up 18% YoY, driven by iPhone 17 Pro ramp and "
                "AI server assembly contracts. Shares rose 3% in Taipei trading. "
                "AAPL supply chain and consumer electronics names may benefit."
            ),
        },
        {
            "headline": "US futures point higher ahead of ISM manufacturing data",
            "source": "CNBC",
            "published_at": "2026-04-01T07:00:00Z",
            "fetched_at": fetched,
            "url": "https://www.cnbc.com/mock/us-futures",
            "body": (
                "S&P 500 futures are up 0.4% and Nasdaq futures up 0.7% as of 7am ET. "
                "ISM manufacturing PMI is due at 10am ET, with consensus at 49.8. "
                "A beat could add to the morning bid; a miss may cap gains."
            ),
        },
        {
            # Intentionally old — should be rejected by freshness filter
            "headline": "Regional bank CRE losses resurface as office delinquencies rise",
            "source": "Bloomberg",
            "published_at": "2026-03-31T22:00:00Z",
            "fetched_at": fetched,
            "url": "https://www.bloomberg.com/mock/cre-losses",
            "body": (
                "New FDIC data shows commercial real estate delinquencies at regional banks "
                "climbed to 4.1% in Q4, the highest since 2012. "
                "KRE ETF fell 1.2% in pre-market. Sentiment on small banks remains cautious."
            ),
        },
        {
            # Intentionally old — should be rejected by freshness filter
            "headline": "Tesla recalls 80,000 vehicles over software defect in FSD system",
            "source": "Reuters",
            "published_at": "2026-03-31T20:30:00Z",
            "fetched_at": fetched,
            "url": "https://www.reuters.com/mock/tesla-recall",
            "body": (
                "NHTSA issued a recall notice for 80,000 Tesla Model 3 and Model Y units "
                "related to a bug in the Full Self-Driving software. "
                "Tesla said an OTA update will be pushed; no physical repair needed."
            ),
        },
        {
            # Intentionally low-credibility source — should be rejected
            "headline": "NVDA to 1000 by end of week say analysts",
            "source": "StockBuzzDaily",
            "published_at": "2026-04-01T07:10:00Z",
            "fetched_at": fetched,
            "url": "https://stockbuzzdaily.com/mock/nvda-prediction",
            "body": "Several unnamed analysts predict NVDA will hit $1000 by Friday.",
        },
    ]
