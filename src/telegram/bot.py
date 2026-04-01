"""
Telegram bot command handler — long-polling loop.

Supported commands:
  /start  — register user and begin receiving briefings
  /stop   — unsubscribe from briefings
"""

import logging
import sys
import time
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import config
from src.telegram.sender import send_message
from src.users import preferences as prefs

logger = logging.getLogger(__name__)

_API_BASE = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}"

_MSG_WELCOME = (
    "안녕하세요! 프리마켓 브리핑 봇입니다.\n\n"
    "장 열리기 전, 오늘 주목할 시장 신호와 뉴스를 짧게 전달해 드립니다.\n\n"
    "등록 완료되었습니다. 다음 브리핑을 기다려 주세요.\n"
    "설정 변경은 웹 UI에서 가능합니다."
)

_MSG_ALREADY_REGISTERED = (
    "이미 등록되어 있습니다. 브리핑이 계속 전송됩니다.\n"
    "구독을 중단하려면 /stop 을 입력하세요."
)

_MSG_STOP = (
    "구독이 취소되었습니다.\n"
    "다시 받으려면 /start 를 입력하세요."
)


def _get_updates(offset: int | None) -> list:
    params: dict = {"timeout": 30, "allowed_updates": ["message"]}
    if offset is not None:
        params["offset"] = offset
    try:
        resp = requests.get(f"{_API_BASE}/getUpdates", params=params, timeout=35)
        resp.raise_for_status()
        return resp.json().get("result", [])
    except Exception as e:
        logger.error("getUpdates failed: %s", e)
        return []


def _handle_update(update: dict) -> None:
    message = update.get("message", {})
    text = (message.get("text") or "").strip()
    chat_id = str(message.get("chat", {}).get("id", ""))

    if not chat_id or not text:
        return

    print(f"[BOT] 메시지 수신: chat_id={chat_id} text={text!r}")

    if text.startswith("/start"):
        is_new = prefs.register_user(chat_id)
        if is_new:
            send_message(_MSG_WELCOME, chat_id=chat_id)
            print(f"[BOT] 신규 유저 등록: {chat_id}")
        else:
            send_message(_MSG_ALREADY_REGISTERED, chat_id=chat_id)
            print(f"[BOT] 이미 등록된 유저: {chat_id}")

    elif text.startswith("/stop"):
        prefs.unregister_user(chat_id)
        send_message(_MSG_STOP, chat_id=chat_id)
        print(f"[BOT] 유저 구독 취소: {chat_id}")


def polling_loop() -> None:
    """Blocking long-polling loop. Run this in a background thread."""
    print("[BOT] 폴링 시작됨.")
    offset: int | None = None
    while True:
        updates = _get_updates(offset)
        for update in updates:
            try:
                _handle_update(update)
            except Exception as e:
                print(f"[BOT] 업데이트 처리 실패 (update_id={update.get('update_id')}): {e}")
            offset = update["update_id"] + 1
        if not updates:
            time.sleep(1)
