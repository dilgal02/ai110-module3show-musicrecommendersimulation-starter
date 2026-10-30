import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

# Point values from the Algorithm Recipe in README.md (max score is 5.0)
GENRE_POINTS = 1.5
MOOD_POINTS = 1.5
ENERGY_POINTS = 1.5
ACOUSTIC_POINTS = 0.5
MAX_SCORE = GENRE_POINTS + MOOD_POINTS + ENERGY_POINTS + ACOUSTIC_POINTS

# Advanced features (Challenge 1). Each rule only counts if the profile sets that preference.
MOOD_TAG_POINTS = 0.5   # per shared tag
MAX_MOOD_TAGS = 2
DECADE_POINTS = 0.5     # half for a neighboring decade
POPULARITY_POINTS = 0.5
INSTRUMENTAL_POINTS = 0.5
EXPLICIT_PENALTY = 1.0

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
    popularity: int = 50
    release_decade: int = 2020
    mood_tags: List[str] = field(default_factory=list)
    instrumentalness: float = 0.0
    explicit: bool = False

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
    mood_tags: List[str] = field(default_factory=list)
    favorite_decade: Optional[int] = None
    target_popularity: Optional[int] = None
    likes_instrumental: Optional[bool] = None
    allow_explicit: bool = True

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
    """Read the songs CSV into a list of dicts, converting numbers, booleans and tag lists."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            # csv gives every value as a string, so convert the numbers for scoring
            for key in ("id", "popularity", "release_decade"):
                row[key] = int(row[key])
            for key in ("energy", "tempo_bpm", "valence", "danceability", "acousticness", "instrumentalness"):
                row[key] = float(row[key])
            row["explicit"] = row["explicit"] == "true"
            row["mood_tags"] = row["mood_tags"].split("|")
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
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

    # Advanced features: a rule is skipped when the profile doesn't set its preference
    wanted_tags = [tag.lower() for tag in user_prefs.get("mood_tags", [])]
    shared = [tag for tag in song["mood_tags"] if tag in wanted_tags][:MAX_MOOD_TAGS]
    if shared:
        points = MOOD_TAG_POINTS * len(shared)
        score += points
        reasons.append(f"mood tags: {', '.join(shared)} (+{points:.2f})")

    if "favorite_decade" in user_prefs:
        decade = song["release_decade"]
        favorite_decade = user_prefs["favorite_decade"]
        if decade == favorite_decade:
            score += DECADE_POINTS
            reasons.append(f"from the {decade}s (+{DECADE_POINTS:.2f})")
        elif abs(decade - favorite_decade) == 10:
            points = DECADE_POINTS / 2
            score += points
            reasons.append(f"from the {decade}s, next to your {favorite_decade}s (+{points:.2f})")

    if "target_popularity" in user_prefs:
        target_popularity = user_prefs["target_popularity"]
        points = POPULARITY_POINTS * (1 - abs(song["popularity"] - target_popularity) / 100)
        score += points
        reasons.append(f"popularity {song['popularity']} vs your {target_popularity} (+{points:.2f})")

    if "likes_instrumental" in user_prefs:
        instrumentalness = song["instrumentalness"]
        if user_prefs["likes_instrumental"]:
            points = INSTRUMENTAL_POINTS * instrumentalness
        else:
            points = INSTRUMENTAL_POINTS * (1 - instrumentalness)
        score += points
        reasons.append(f"instrumentalness {instrumentalness:.2f} (+{points:.2f})")

    if not user_prefs.get("allow_explicit", True) and song["explicit"]:
        score -= EXPLICIT_PENALTY
        reasons.append(f"explicit lyrics (-{EXPLICIT_PENALTY:.2f})")

    return score, reasons

def max_score(user_prefs: Dict) -> float:
    """Return the best possible score for this profile, counting only the rules it uses."""
    total = MAX_SCORE
    total += MOOD_TAG_POINTS * min(len(user_prefs.get("mood_tags", [])), MAX_MOOD_TAGS)
    if "favorite_decade" in user_prefs:
        total += DECADE_POINTS
    if "target_popularity" in user_prefs:
        total += POPULARITY_POINTS
    if "likes_instrumental" in user_prefs:
        total += INSTRUMENTAL_POINTS
    return total

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort from highest to lowest, and return the top k as (song, score, explanation)."""
    # judge every song, then rank; sorted() is stable, so ties keep their CSV order
    judged = [(song, *score_song(user_prefs, song)) for song in songs]
    ranked = sorted(judged, key=lambda item: item[1], reverse=True)
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
