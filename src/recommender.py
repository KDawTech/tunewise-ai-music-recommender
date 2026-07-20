import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Song:
    """Represents a song and its musical attributes."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's music preferences."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """Ranks songs according to a user's taste profile."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _score(self, user: UserProfile, song: Song) -> float:
        score = 0.0

        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0

        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.0

        energy_similarity = max(
            0.0,
            1.0 - abs(song.energy - user.target_energy),
        )
        score += energy_similarity

        if user.likes_acoustic:
            score += song.acousticness
        else:
            score += 1.0 - song.acousticness

        return score

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs ranked by preference score."""

        ranked_songs = sorted(
            self.songs,
            key=lambda song: self._score(user, song),
            reverse=True,
        )

        return ranked_songs[:k]

    def explain_recommendation(
        self,
        user: UserProfile,
        song: Song,
    ) -> str:
        """Explains why a song matches the user's preferences."""

        reasons = []

        if song.genre.lower() == user.favorite_genre.lower():
            reasons.append("genre matches your preference")

        if song.mood.lower() == user.favorite_mood.lower():
            reasons.append("mood matches your preference")

        energy_difference = abs(song.energy - user.target_energy)

        if energy_difference <= 0.15:
            reasons.append("energy level is close to your target")

        if user.likes_acoustic and song.acousticness >= 0.6:
            reasons.append("it has a strong acoustic sound")
        elif not user.likes_acoustic and song.acousticness < 0.6:
            reasons.append("it has a less acoustic sound")

        if not reasons:
            reasons.append("it received a competitive overall score")

        return ", ".join(reasons).capitalize() + "."


def load_songs(csv_path: str) -> List[Dict]:
    """Loads song information from a CSV file."""

    songs = []

    with open(csv_path, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])

            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(
    user_prefs: Dict,
    song: Dict,
) -> Tuple[float, List[str]]:
    """Calculates a song's score and explains each awarded point."""

    score = 0.0
    reasons = []

    preferred_genre = str(user_prefs.get("genre", "")).lower()
    preferred_mood = str(user_prefs.get("mood", "")).lower()
    target_energy = float(user_prefs.get("energy", 0.5))

    if song["genre"].lower() == preferred_genre:
        score += 2.0
        reasons.append("genre match (+2.00)")

    if song["mood"].lower() == preferred_mood:
        score += 1.0
        reasons.append("mood match (+1.00)")

    energy_difference = abs(song["energy"] - target_energy)
    energy_points = max(0.0, 1.0 - energy_difference)

    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
) -> List[Tuple[Dict, float, str]]:
    """Scores all songs and returns the top k recommendations."""

    scored_songs = []

    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))

    ranked_songs = sorted(
        scored_songs,
        key=lambda result: result[1],
        reverse=True,
    )

    return ranked_songs[:k]