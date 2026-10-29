import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Point values from the Algorithm Recipe in README.md (max score is 5.0)
GENRE_POINTS = 1.5
MOOD_POINTS = 1.5
ENERGY_POINTS = 1.5
ACOUSTIC_POINTS = 0.5
MAX_SCORE = GENRE_POINTS + MOOD_POINTS + ENERGY_POINTS + ACOUSTIC_POINTS

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # csv gives every value as a string, so convert the numbers for scoring
            row["id"] = int(row["id"])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    score = 0.0
    reasons = []

    genre = song["genre"].lower()
    favorite_genre = user_prefs["favorite_genre"].lower()
    if genre == favorite_genre:
        score += GENRE_POINTS
        reasons.append(f"genre match: {genre} (+{GENRE_POINTS:.2f})")
    elif favorite_genre and (favorite_genre in genre or genre in favorite_genre):
        # partial match, e.g. "pop" and "indie pop"
        points = GENRE_POINTS / 2
        score += points
        reasons.append(f"similar genre: {genre} (+{points:.2f})")

    mood = song["mood"].lower()
    if mood == user_prefs["favorite_mood"].lower():
        score += MOOD_POINTS
        reasons.append(f"mood match: {mood} (+{MOOD_POINTS:.2f})")

    # closer to the target is better, not higher
    target_energy = user_prefs["target_energy"]
    points = ENERGY_POINTS * (1 - abs(song["energy"] - target_energy))
    score += points
    reasons.append(f"energy {song['energy']:.2f} vs your {target_energy:.2f} (+{points:.2f})")

    acousticness = song["acousticness"]
    if user_prefs["likes_acoustic"]:
        points = ACOUSTIC_POINTS * acousticness
    else:
        points = ACOUSTIC_POINTS * (1 - acousticness)
    score += points
    reasons.append(f"acousticness {acousticness:.2f} (+{points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # judge every song, then rank; sorted() is stable, so ties keep their CSV order
    judged = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(judged, key=lambda item: item[1], reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
