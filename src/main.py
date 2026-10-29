"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, MAX_SCORE

WIDTH = 60

# Keys match the UserProfile fields so both versions of the recommender use the same profile.
PROFILES = {
    # the starter example profile
    "Default pop/happy": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    },
    # my taste profile: a late-night study listener who wants calm, acoustic-leaning lofi
    "Late-night study": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
}


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    acoustic = "likes acoustic" if user_prefs["likes_acoustic"] else "prefers electronic"
    print(f"\nTop {len(recommendations)} for: {name}")
    print(f"  {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / "
          f"energy {user_prefs['target_energy']:.2f} / {acoustic}")
    print("=" * WIDTH)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        heading = f"{rank:>2}. {song['title']} by {song['artist']}"
        print(f"{heading:<48} {score:.2f} / {MAX_SCORE:.2f}")
        # recommend_songs joins the reasons with "; ", so split them back into lines
        for reason in explanation.split("; "):
            print(f"      + {reason}")
        print("-" * WIDTH)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
