"""Command-line runner for the Music Recommender Simulation."""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")

    profiles = [
        {
            "name": "High-Energy Pop",
            "genre": "pop",
            "mood": "happy",
            "energy": 0.8,
        },
        {
            "name": "Chill Lofi",
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.35,
        },
        {
            "name": "Intense Rock",
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
        },
    ]

    for profile in profiles:
        print(f"\n{'=' * 55}")
        print(f"User Profile: {profile['name']}")
        print(
            f"Genre: {profile['genre']} | "
            f"Mood: {profile['mood']} | "
            f"Energy: {profile['energy']}"
        )
        print("=" * 55)

        recommendations = recommend_songs(profile, songs, k=5)

        for position, (song, score, explanation) in enumerate(
            recommendations,
            start=1,
        ):
            print(
                f"\n{position}. {song['title']} by {song['artist']}"
                f" - Score: {score:.2f}"
            )
            print(f"   Because: {explanation}")


if __name__ == "__main__":
    main()