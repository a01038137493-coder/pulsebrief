"""
Scheduler — runs pipeline at the interval set in user preferences.

Usage:
    python src/scheduler/loop.py
"""

import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.pipeline.run import main as run_pipeline
from src.users import preferences as prefs


def loop() -> None:
    print("스케줄러 시작. Ctrl+C로 종료.\n")

    while True:
        user_prefs = prefs.load()
        interval = int(user_prefs.get("interval_minutes", 10))

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 발송 시작 (인터벌: {interval}분)")
        try:
            run_pipeline()
            print(f"발송 완료. 다음 발송까지 {interval}분 대기...\n")
        except Exception as e:
            print(f"[ERROR] {e}\n다음 발송까지 {interval}분 대기...\n")

        time.sleep(interval * 60)


if __name__ == "__main__":
    loop()
