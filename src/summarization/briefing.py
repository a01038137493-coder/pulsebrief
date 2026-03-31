# -*- coding: utf-8 -*-
"""
Calls Claude with the briefing system prompt and a list of news items.
Returns a parsed briefing dict matching the schema in prompts/briefing.md.
"""

import json
import time
from pathlib import Path

import anthropic

import config

_PROMPT_PATH = Path(__file__).parent.parent.parent / "prompts" / "briefing.md"
_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def _load_system_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _format_news_for_prompt(news_items: list[dict]) -> str:
    lines = []
    for i, item in enumerate(news_items, start=1):
        lines.append(f"[{i}] {item['headline']}")
        lines.append(f"    Source: {item['source']} | Published: {item['published_at']}")
        lines.append(f"    {item['body']}")
        lines.append("")
    return "\n".join(lines)


def generate_briefing(
    news_items: list[dict],
    market: str = "US Equities",
    watchlist: list[str] | None = None,
    sectors: list[str] | None = None,
) -> dict:
    system_prompt = _load_system_prompt()

    personalization = ""
    if watchlist:
        personalization += f"User watchlist: {', '.join(watchlist)}\n"
    if sectors:
        personalization += f"User sector interests: {', '.join(sectors)}\n"
    if personalization:
        personalization = f"Personalization context (prioritize these):\n{personalization}\n"

    user_message = (
        f"Market: {market}\n\n"
        f"{personalization}"
        f"News items:\n\n"
        f"{_format_news_for_prompt(news_items)}\n\n"
        f"Generate the pre-market briefing JSON. Write all text fields in Korean."
    )

    for attempt in range(4):
        try:
            response = _client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            break
        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt < 3:
                wait = 10 * (attempt + 1)
                print(f"  API overloaded, retry in {wait}s ({attempt+1}/3)...")
                time.sleep(wait)
            else:
                raise

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
