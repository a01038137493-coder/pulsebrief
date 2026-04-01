"""
End-to-end pipeline entry point.

Run with:
    python src/pipeline/run.py

Steps:
    1. Load news (shared across all users)
    2. Filter: freshness, credibility, duplicates
    3. For each registered user:
       a. Generate personalized briefing via Claude
       b. Session freshness re-check
       c. Format for Telegram
       d. Send message
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config
from src.ingestion.sources import get_all_news
from src.ranking.filter import filter_news, is_briefing_fresh
from src.summarization.briefing import generate_briefing
from src.telegram.formatter import format_for_telegram
from src.telegram.sender import send_message
from src.users import preferences as prefs


def _send_briefing_to_user(chat_id: str, user_prefs: dict, accepted: list, briefing_generated_at: datetime) -> None:
    print(f"  → User {chat_id}")

    briefing = generate_briefing(
        accepted,
        market=user_prefs.get("target_market", "US Equities"),
        watchlist=user_prefs.get("watchlist"),
        sectors=user_prefs.get("sectors"),
    )

    if not is_briefing_fresh(briefing_generated_at):
        print(f"    [SKIP] Briefing too old for {chat_id}")
        return

    message = format_for_telegram(briefing)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_message(f"{message}\n\n🕐 {timestamp}", chat_id=chat_id)
    print(f"    Sent.")


def main() -> None:
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

    briefing_generated_at = datetime.now(timezone.utc)

    # Determine target users: registered users, or fall back to the env-configured chat ID
    user_ids = prefs.list_users()
    if user_ids:
        user_prefs_map = {uid: prefs.load_user(uid) for uid in user_ids}
    else:
        # Legacy single-user fallback
        user_ids = [config.TELEGRAM_CHAT_ID]
        user_prefs_map = {config.TELEGRAM_CHAT_ID: prefs.load()}

    print(f"=== Step 3–6: Generating and sending to {len(user_ids)} user(s) ===")
    print(json.dumps({"user_count": len(user_ids)}, ensure_ascii=False))
    print()

    for chat_id in user_ids:
        try:
            _send_briefing_to_user(chat_id, user_prefs_map[chat_id], accepted, briefing_generated_at)
        except Exception as e:
            print(f"  [ERROR] Failed for user {chat_id}: {e}")

    print("\nDone.")


if __name__ == "__main__":
    main()
