"""
Sends a plain text message to a Telegram chat via the Bot API.
This is the only file that touches the Telegram API.
"""

import requests

import config

_TELEGRAM_API = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"


def send_message(text: str, chat_id: str = config.TELEGRAM_CHAT_ID) -> None:
    response = requests.post(
        _TELEGRAM_API,
        json={"chat_id": chat_id, "text": text},
        timeout=10,
    )
    response.raise_for_status()
