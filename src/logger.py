"""Structured interaction logging for TuneWise."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


Recommendation = tuple[dict[str, Any], float, str]


def log_interaction(
    preferences: dict[str, Any],
    recommendations: list[Recommendation],
    ai_result: dict[str, Any],
    log_path: str = "logs/interactions.jsonl",
) -> None:
    """Append one reproducible interaction record as JSON Lines."""

    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "preferences": preferences,
        "recommendations": [
            {
                "id": int(song["id"]),
                "title": song["title"],
                "artist": song["artist"],
                "score": round(float(score), 3),
            }
            for song, score, _explanation in recommendations
        ],
        "ai": {
            "provider": ai_result.get("provider"),
            "model": ai_result.get("model"),
            "used_fallback": ai_result.get("used_fallback"),
            "error": ai_result.get("error"),
        },
    }

    with path.open(
        mode="a",
        encoding="utf-8",
    ) as file:
        file.write(json.dumps(record) + "\n")