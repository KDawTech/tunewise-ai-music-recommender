import pytest

from src.guardrails import (
    sanitize_ai_payload,
    validate_preferences,
)


def test_validate_preferences_normalizes_input():
    result = validate_preferences(
        {
            "genre": " Pop ",
            "mood": " Happy ",
            "energy": 0.8,
            "likes_acoustic": False,
        },
        k=5,
    )

    assert result["genre"] == "pop"
    assert result["mood"] == "happy"
    assert result["energy"] == 0.8
    assert result["likes_acoustic"] is False


def test_validate_preferences_rejects_invalid_energy():
    with pytest.raises(ValueError):
        validate_preferences(
            {
                "genre": "pop",
                "mood": "happy",
                "energy": 1.5,
            }
        )


def test_sanitize_ai_payload_removes_unknown_song():
    payload = {
        "summary": "Test recommendations",
        "recommendations": [
            {
                "id": 1,
                "reason": "Matches the requested mood.",
            },
            {
                "id": 999,
                "reason": "This song does not exist.",
            },
        ],
    }

    summary, reasons = sanitize_ai_payload(
        payload,
        allowed_song_ids={1, 2},
    )

    assert summary == "Test recommendations"
    assert 1 in reasons
    assert 999 not in reasons


def test_sanitize_ai_payload_removes_duplicates():
    payload = {
        "summary": "Test",
        "recommendations": [
            {
                "id": 1,
                "reason": "First explanation.",
            },
            {
                "id": 1,
                "reason": "Duplicate explanation.",
            },
        ],
    }

    _summary, reasons = sanitize_ai_payload(
        payload,
        allowed_song_ids={1},
    )

    assert len(reasons) == 1
    assert reasons[1] == "First explanation."