# -*- coding: utf-8 -*-
"""
Flask settings page + API for the pre-market briefing bot.
Scheduler runs in a background thread alongside the web server.

Run locally:
    python src/web/app.py
"""

import os
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from flask import Flask, jsonify, render_template, request

from src.users import preferences as prefs

app = Flask(__name__, template_folder="templates")


# --- Background scheduler ---------------------------------------------------

def _scheduler_loop():
    from datetime import datetime
    from src.pipeline.run import main as run_pipeline

    print("스케줄러 시작됨.")
    while True:
        try:
            user_prefs = prefs.load()
            interval = int(user_prefs.get("interval_minutes", 10))
            print(f"[{datetime.now().strftime('%H:%M:%S')}] 발송 시작 (인터벌: {interval}분)")
            run_pipeline()
            print(f"발송 완료. {interval}분 대기...")
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"[ERROR] {e}")
            interval = 10
        time.sleep(interval * 60)


def start_scheduler():
    t = threading.Thread(target=_scheduler_loop, daemon=True)
    t.start()


# --- Routes -----------------------------------------------------------------

@app.get("/")
def index():
    return render_template("settings.html", prefs=prefs.load())


@app.post("/save")
def save():
    data = request.get_json(force=True)
    updated = {
        "watchlist": [t.strip().upper() for t in data.get("watchlist", []) if t.strip()],
        "sectors": [s.strip().lower() for s in data.get("sectors", []) if s.strip()],
        "target_market": data.get("target_market", "US Equities"),
        "interval_minutes": int(data.get("interval_minutes", 10)),
        "urgent_alerts": bool(data.get("urgent_alerts", False)),
    }
    prefs.save(updated)
    return jsonify({"ok": True})


@app.post("/send")
def send_now():
    def run():
        from src.pipeline.run import main
        try:
            main()
        except Exception as e:
            import traceback
            traceback.print_exc()

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"ok": True})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    start_scheduler()
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
