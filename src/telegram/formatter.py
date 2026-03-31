# -*- coding: utf-8 -*-
"""
Calls Claude with the Telegram format prompt and a briefing dict.
Returns a plain text string ready to send via the Telegram Bot API.
"""

import json
import time
from pathlib import Path

import anthropic

import config

_PROMPT_PATH = Path(__file__).parent / "prompts" / "telegram_format.md"
_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def _load_system_prompt() -> str:
    return _PROMPT_PATH.read_text(encoding="utf-8")


def format_for_telegram(briefing: dict) -> str:
    system_prompt = _load_system_prompt()
    user_message = (
        "Format the following briefing as a Telegram message. Write everything in Korean.\n\n"
        f"{json.dumps(briefing, indent=2, ensure_ascii=False)}"
    )

    for attempt in range(4):
        try:
            response = _client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=512,
                system=system_prompt,
                messages=[{"role": "user", "content": user_message}],
            )
            return response.content[0].text.strip()
        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt < 3:
                wait = 10 * (attempt + 1)
                print(f"  API overloaded, retry in {wait}s ({attempt+1}/3)...")
                time.sleep(wait)
            else:
                raise
