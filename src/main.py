"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse
import textwrap

from src.recommender import (load_songs, recommend_songs, max_score, MODES,
                             ARTIST_PENALTY, GENRE_PENALTY)

WIDTH = 60
TABLE_WIDTHS = [2, 24, 6, 42]  # rank, song + artist, score, reasons

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


def print_header(name: str, user_prefs: dict, count: int) -> None:
    """Print the profile name and the preferences it was scored with."""
    acoustic = "likes acoustic" if user_prefs["likes_acoustic"] else "prefers electronic"
    print(f"\nTop {count} for: {name}")
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


def print_recommendations(name: str, user_prefs: dict, recommendations: list, best: float) -> None:
    """Print one profile's recommendations with their scores and reasons."""
    print_header(name, user_prefs, len(recommendations))
    print("=" * WIDTH)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        heading = f"{rank:>2}. {song['title']} by {song['artist']}"
        print(f"{heading:<48} {score:.2f} / {best:.2f}")
        # recommend_songs joins the reasons with "; ", so split them back into lines
        for reason in explanation.split("; "):
            print(f"      + {reason}")
        print("-" * WIDTH)


def render_table(headers: list, rows: list, widths: list) -> str:
    """Draw an ASCII grid where every cell is a list of lines, wrapping lines that are too long."""
    def border(char: str) -> str:
        return "+" + "+".join(char * (width + 2) for width in widths) + "+"

    def line(cells: list) -> str:
        return "|" + "|".join(f" {cell:<{width}} " for cell, width in zip(cells, widths)) + "|"

    out = [border("-"), line(headers), border("=")]
    for row in rows:
        cells = []
        for lines, width in zip(row, widths):
            wrapped = []
            for text in lines:
                wrapped += textwrap.wrap(text, width, subsequent_indent="  ") if len(text) > width else [text]
            cells.append(wrapped)
        for i in range(max(len(cell) for cell in cells)):
            out.append(line([cell[i] if i < len(cell) else "" for cell in cells]))
        out.append(border("-"))
    return "\n".join(out)


def print_table(name: str, user_prefs: dict, recommendations: list, best: float) -> None:
    """Print one profile's recommendations as a table, with every reason on its own line."""
    print_header(name, user_prefs, len(recommendations))
    rows = [[[str(rank)],
             [song["title"], f"by {song['artist']}"],
             [f"{score:>6.2f}", f"/ {best:.2f}"],
             explanation.split("; ")]
            for rank, (song, score, explanation) in enumerate(recommendations, start=1)]
    print(render_table(["#", "Song", "Score", "Reasons"], rows, TABLE_WIDTHS))


def main() -> None:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", choices=MODES, default="balanced",
                        help="ranking strategy to use (default: balanced)")
    parser.add_argument("--diverse", action="store_true",
                        help="penalize artists and genres that are already in the top list")
    parser.add_argument("--table", action="store_true",
                        help="show each profile's top songs as a summary table")
    args = parser.parse_args()
    mode = MODES[args.mode]

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Scoring mode: {mode.name} - {mode.description}")
    if args.diverse:
        print(f"Diversity penalty: on (-{ARTIST_PENALTY:.2f} per repeated artist, "
              f"-{GENRE_PENALTY:.2f} per repeated genre)")

    show = print_table if args.table else print_recommendations
    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5, mode=mode, diverse=args.diverse)
        show(name, user_prefs, recommendations, max_score(user_prefs, mode))


if __name__ == "__main__":
    main()
