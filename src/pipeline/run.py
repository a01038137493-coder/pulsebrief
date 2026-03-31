"""
End-to-end mock pipeline entry point.

Run with:
    python src/pipeline/run.py

Steps:
    1. Load mock news
    2. Filter: freshness, credibility, duplicates
    3. Generate structured briefing via Claude
    4. Session freshness re-check
    5. Format briefing for Telegram via Claude
    6. Send message to configured Telegram chat
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# Allow imports from project root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ingestion.sources import get_all_news
from src.ranking.filter import filter_news, is_briefing_fresh
from src.summarization.briefing import generate_briefing
from src.telegram.formatter import format_for_telegram
from src.telegram.sender import send_message
from src.users import preferences as prefs


def main() -> None:
    user_prefs = prefs.load()

    print("=== Step 1: Loading news ===")
    news_items = get_all_news()
    print(f"Fetched {len(news_items)} items\n")

    print("=== Step 2: Filtering ===")
    accepted, rejected = filter_news(news_items)
    for item in rejected:
        print(f"  [REJECTED] {item['headline'][:60]}  —  {item['rejected_reason']}")
    print(f"  Accepted: {len(accepted)}  Rejected: {len(rejected)}\n")

    if not accepted:
        print("No items passed the filter. Nothing to send.")
        return

    print("=== Step 3: Generating briefing ===")
    if user_prefs.get("watchlist"):
        print(f"  Watchlist: {user_prefs['watchlist']}")
    briefing_generated_at = datetime.now(timezone.utc)
    briefing = generate_briefing(
        accepted,
        market=user_prefs.get("target_market", "US Equities"),
        watchlist=user_prefs.get("watchlist"),
        sectors=user_prefs.get("sectors"),
    )
    print(json.dumps(briefing, indent=2, ensure_ascii=False))
    print()

    print("=== Step 4: Session freshness re-check ===")
    if not is_briefing_fresh(briefing_generated_at):
        print("Briefing is too old to send. Aborting.")
        return
    print("  Fresh. Proceeding.\n")

    print("=== Step 5: Formatting for Telegram ===")
    message = format_for_telegram(briefing)
    print(message)
    print()

    print("=== Step 6: Sending to Telegram ===")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_message(f"{message}\n\n🕐 {timestamp}")
    print("Sent.")


if __name__ == "__main__":
    main()
