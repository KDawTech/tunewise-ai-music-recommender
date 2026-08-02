"""Streamlit interface for the TuneWise AI Music Recommender."""

from pathlib import Path

import streamlit as st

from src.ai_service import generate_ai_explanations
from src.guardrails import validate_preferences
from src.logger import log_interaction
from src.recommender import load_songs, recommend_songs


PROJECT_ROOT = Path(__file__).resolve().parent
SONGS_PATH = PROJECT_ROOT / "data" / "songs.csv"


@st.cache_data
def get_songs():
    """Load and cache the local song catalog."""

    return load_songs(str(SONGS_PATH))


st.set_page_config(
    page_title="TuneWise",
    page_icon="🎵",
    layout="wide",
)

st.title("🎵 TuneWise")
st.subheader("AI-Powered Music Recommendation System")

st.write(
    "Choose your music preferences and TuneWise will retrieve, rank, "
    "and explain songs from its verified catalog."
)

songs = get_songs()

genres = sorted({song["genre"] for song in songs})
moods = sorted({song["mood"] for song in songs})

with st.form("recommendation_form"):
    left, right = st.columns(2)

    with left:
        selected_genre = st.selectbox(
            "Favorite genre",
            genres,
        )

        selected_mood = st.selectbox(
            "Preferred mood",
            moods,
        )

    with right:
        target_energy = st.slider(
            "Target energy",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
        )

        likes_acoustic = st.checkbox(
            "Prefer acoustic music",
            value=False,
        )

    recommendation_count = st.slider(
        "Number of recommendations",
        min_value=1,
        max_value=10,
        value=5,
    )

    submitted = st.form_submit_button(
        "Generate Recommendations",
        use_container_width=True,
    )

if submitted:
    raw_preferences = {
        "genre": selected_genre,
        "mood": selected_mood,
        "energy": target_energy,
        "likes_acoustic": likes_acoustic,
    }

    try:
        preferences = validate_preferences(
            raw_preferences,
            k=recommendation_count,
        )

        recommendations = recommend_songs(
            preferences,
            songs,
            k=recommendation_count,
        )

        ai_result = generate_ai_explanations(
            preferences,
            recommendations,
        )

        log_interaction(
            preferences,
            recommendations,
            ai_result,
        )

    except ValueError as error:
        st.error(str(error))

    except Exception as error:
        st.error(f"Unable to generate recommendations: {error}")

    else:
        st.divider()
        st.subheader("Your Recommendations")
        st.write(ai_result["summary"])

        if ai_result["used_fallback"]:
            st.warning(
                "AI explanations are unavailable, so TuneWise is using "
                "its reliable rule-based explanations."
            )
        else:
            st.success(
                f"Explanations generated using {ai_result['model']}."
            )

        for position, (song, score, original_reason) in enumerate(
            recommendations,
            start=1,
        ):
            song_id = int(song["id"])

            ai_reason = ai_result["reasons"].get(
                song_id,
                original_reason,
            )

            confidence = min(
                100,
                max(0, round((score / 5.0) * 100)),
            )

            with st.container(border=True):
                st.markdown(
                    f"### {position}. {song['title']} — {song['artist']}"
                )

                col1, col2, col3, col4 = st.columns(4)

                col1.metric("Genre", song["genre"].title())
                col2.metric("Mood", song["mood"].title())
                col3.metric("Energy", f"{song['energy']:.2f}")
                col4.metric("Match", f"{confidence}%")

                st.progress(confidence / 100)

                st.write(f"**Why it fits:** {ai_reason}")

                st.caption(
                    f"Tempo: {song['tempo_bpm']:.0f} BPM · "
                    f"Danceability: {song['danceability']:.2f} · "
                    f"Acousticness: {song['acousticness']:.2f}"
                )

st.divider()

st.caption(
    "TuneWise only displays songs retrieved from its local verified catalog. "
    "AI-generated song IDs are validated before results are shown."
)