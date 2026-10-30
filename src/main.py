"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, max_score

WIDTH = 60

# Keys match the UserProfile fields so both versions of the recommender use the same profile.
PROFILES = {
    # the starter example profile
    "High-Energy Pop": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
    },
    # my taste profile: a late-night study listener who wants calm, acoustic-leaning lofi
    "Chill Lofi": {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "likes_acoustic": True,
    },
    # the opposite of Chill Lofi on every feature
    "Deep Intense Rock": {
        "favorite_genre": "rock",
        "favorite_mood": "intense",
        "target_energy": 0.90,
        "likes_acoustic": False,
    },
    # High-Energy Pop plus every advanced preference from Challenge 1
    "Family Road Trip": {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
        "likes_acoustic": False,
        "mood_tags": ["sunny", "uplifting", "warm"],
        "favorite_decade": 2010,
        "target_popularity": 80,
        "likes_instrumental": False,
        "allow_explicit": False,
    },
}


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print one profile's recommendations with their scores and reasons."""
    acoustic = "likes acoustic" if user_prefs["likes_acoustic"] else "prefers electronic"
    print(f"\nTop {len(recommendations)} for: {name}")
    print(f"  {user_prefs['favorite_genre']} / {user_prefs['favorite_mood']} / "
          f"energy {user_prefs['target_energy']:.2f} / {acoustic}")
    # advanced preferences are optional, so only show the ones this profile sets
    extras = []
    if user_prefs.get("mood_tags"):
        extras.append("mood tags: " + ", ".join(user_prefs["mood_tags"]))
    if "favorite_decade" in user_prefs:
        extras.append(f"decade: {user_prefs['favorite_decade']}s")
    if "target_popularity" in user_prefs:
        extras.append(f"popularity: {user_prefs['target_popularity']}")
    if "likes_instrumental" in user_prefs:
        extras.append("likes instrumental" if user_prefs["likes_instrumental"] else "prefers vocals")
    if not user_prefs.get("allow_explicit", True):
        extras.append("no explicit lyrics")
    for extra in extras:
        print(f"  {extra}")
    print("=" * WIDTH)
    best = max_score(user_prefs)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        heading = f"{rank:>2}. {song['title']} by {song['artist']}"
        print(f"{heading:<48} {score:.2f} / {best:.2f}")
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
