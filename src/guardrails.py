"""Validation and safety guardrails for TuneWise."""

from __future__ import annotations

from typing import Any


def validate_preferences(
    preferences: dict[str, Any],
    k: int = 5,
) -> dict[str, Any]:
    """Validate and normalize a user's music preferences."""

    genre = str(preferences.get("genre", "")).strip().lower()
    mood = str(preferences.get("mood", "")).strip().lower()

    if not genre:
        raise ValueError("Genre is required.")

    if not mood:
        raise ValueError("Mood is required.")

    try:
        energy = float(preferences.get("energy", 0.5))
    except (TypeError, ValueError) as exc:
        raise ValueError("Energy must be a number.") from exc

    if not 0.0 <= energy <= 1.0:
        raise ValueError("Energy must be between 0.0 and 1.0.")

    if not 1 <= int(k) <= 10:
        raise ValueError("Number of recommendations must be between 1 and 10.")

    return {
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "likes_acoustic": bool(
            preferences.get("likes_acoustic", False)
        ),
    }


def sanitize_ai_payload(
    payload: Any,
    allowed_song_ids: set[int],
) -> tuple[str, dict[int, str]]:
    """
    Keep only explanations connected to retrieved songs.

    Any unknown or fabricated song ID is removed.
    """

    if not isinstance(payload, dict):
        return (
            "Recommendations were generated from the retrieved catalog.",
            {},
        )

    summary = str(payload.get("summary", "")).strip()

    if not summary:
        summary = "Recommendations were generated from the retrieved catalog."

    summary = summary[:600]

    raw_recommendations = payload.get("recommendations", [])

    if not isinstance(raw_recommendations, list):
        raw_recommendations = []

    reasons: dict[int, str] = {}
    seen_ids: set[int] = set()

    for item in raw_recommendations:
        if not isinstance(item, dict):
            continue

        try:
            song_id = int(item.get("id"))
        except (TypeError, ValueError):
            continue

        reason = str(item.get("reason", "")).strip()

        if (
            song_id not in allowed_song_ids
            or song_id in seen_ids
            or not reason
        ):
            continue

        reasons[song_id] = reason[:400]
        seen_ids.add(song_id)

    return summary, reasons