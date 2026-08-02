"""Groq-powered explanations grounded in retrieved TuneWise songs."""

from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from .guardrails import sanitize_ai_payload


load_dotenv()


Recommendation = tuple[
    dict[str, Any],
    float,
    str,
]


def _build_verified_summary(
    preferences: dict[str, Any],
) -> str:
    """Create a deterministic summary without AI-generated claims."""

    genre = str(
        preferences.get("genre", "selected")
    ).title()

    mood = str(
        preferences.get("mood", "selected")
    ).title()

    energy = float(
        preferences.get("energy", 0.5)
    )

    likes_acoustic = bool(
        preferences.get("likes_acoustic", False)
    )

    acoustic_text = (
        "a preference for acoustic music"
        if likes_acoustic
        else "a preference for less-acoustic music"
    )

    return (
        f"TuneWise ranked songs from its verified catalog using the "
        f"{genre} genre, {mood} mood, a target energy of "
        f"{energy:.2f}, and {acoustic_text}."
    )


def _fallback_result(
    preferences: dict[str, Any],
    recommendations: list[Recommendation],
    error: str | None = None,
) -> dict[str, Any]:
    """Return deterministic explanations if Groq is unavailable."""

    reasons = {
        int(song["id"]): explanation
        for song, _score, explanation in recommendations
    }

    return {
        "summary": _build_verified_summary(preferences),
        "reasons": reasons,
        "provider": "rule-based fallback",
        "model": None,
        "used_fallback": True,
        "error": error,
    }


def generate_ai_explanations(
    preferences: dict[str, Any],
    recommendations: list[Recommendation],
) -> dict[str, Any]:
    """
    Generate explanations grounded only in retrieved catalog data.

    The model may rewrite verified reasons, but it cannot select new songs
    or change the recommendation ranking.
    """

    if not recommendations:
        return {
            "summary": "No matching recommendations were found.",
            "reasons": {},
            "provider": "none",
            "model": None,
            "used_fallback": True,
            "error": None,
        }

    api_key = os.getenv(
        "GROQ_API_KEY",
        "",
    ).strip()

    if not api_key:
        return _fallback_result(
            preferences,
            recommendations,
            error="GROQ_API_KEY is not configured.",
        )

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b",
    ).strip()

    retrieved_context = [
        {
            "id": int(song["id"]),
            "title": song["title"],
            "artist": song["artist"],
            "genre": song["genre"],
            "mood": song["mood"],
            "energy": song["energy"],
            "tempo_bpm": song["tempo_bpm"],
            "valence": song["valence"],
            "danceability": song["danceability"],
            "acousticness": song["acousticness"],
            "ranking_score": round(score, 3),
            "verified_reason": explanation,
        }
        for song, score, explanation in recommendations
    ]

    allowed_ids = {
        int(song["id"])
        for song, _score, _explanation in recommendations
    }

    prompt_data = {
        "user_preferences": preferences,
        "retrieved_songs": retrieved_context,
    }

    system_message = """
You are TuneWise, a grounded music recommendation assistant.

Rewrite each supplied verified_reason as one short, natural sentence.

Rules:
1. Use only songs supplied in retrieved_songs.
2. Use only facts explicitly stated in verified_reason.
3. Preserve the meaning and strength of every statement.
4. Do not change a weak similarity into a strong match.
5. Do not describe a negative result as a preference match.
6. Preserve phrases such as "more acoustic than preferred,"
   "less acoustic than preferred," "weak energy similarity,"
   and "genre does not match."
7. Never independently interpret numeric attributes.
8. Never claim that energy values are close unless verified_reason
   labels the energy similarity as strong or moderate.
9. Never invent a song, artist, ID, preference, or musical attribute.
10. Put the numeric song ID only in the id field.
11. Do not write phrases such as "Song 6" inside the reason.
12. Do not mention scoring points in the rewritten reason.
13. Return one explanation for every retrieved song.
14. Return valid JSON matching the required schema.
""".strip()

    response_schema = {
        "type": "json_schema",
        "json_schema": {
            "name": "tunewise_recommendations",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                    },
                    "recommendations": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {
                                    "type": "integer",
                                },
                                "reason": {
                                    "type": "string",
                                },
                            },
                            "required": [
                                "id",
                                "reason",
                            ],
                            "additionalProperties": False,
                        },
                    },
                },
                "required": [
                    "summary",
                    "recommendations",
                ],
                "additionalProperties": False,
            },
        },
    }

    try:
        client = Groq(
            api_key=api_key,
        )

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        prompt_data,
                        indent=2,
                    ),
                },
            ],
            response_format=response_schema,
            reasoning_effort="low",
            temperature=0.1,
        )

        content = completion.choices[0].message.content

        if not content:
            raise ValueError(
                "The AI returned an empty response."
            )

        payload = json.loads(content)

        _ai_summary, reasons = sanitize_ai_payload(
            payload,
            allowed_ids,
        )

        # Add deterministic explanations if the AI omits any song.
        for song, _score, explanation in recommendations:
            song_id = int(song["id"])

            reasons.setdefault(
                song_id,
                explanation,
            )

        return {
            "summary": _build_verified_summary(preferences),
            "reasons": reasons,
            "provider": "Groq",
            "model": model,
            "used_fallback": False,
            "error": None,
        }

    except Exception as exc:
        return _fallback_result(
            preferences,
            recommendations,
            error=str(exc),
        )