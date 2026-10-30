# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Before this project I thought Spotify just looked at what genre I listen to. It turns out real platforms mix two ideas. Collaborative filtering looks at what other people with a similar listening history play, skip and add to playlists, so it can suggest songs I would never find on my own. Content-based filtering looks at the song itself (genre, tempo, energy, how "happy" it sounds) and finds tracks that are similar to the ones I already like. Spotify and YouTube use both at the same time, plus a lot of behavior data like skips and watch time. My simulation only has a CSV with 20 songs and no data about other users, so I'm building a content-based recommender. Genre and mood count the same, and after that it looks at how close the song's energy is to what the user wants. I care about "close to" and not "higher", because if someone wants chill music, the most energetic song in the list is the worst pick for them, not the best.

**Song features I use in the score:**

- `genre` - exact match gets full points, a partial match like "pop" and "indie pop" gets half
- `mood` - exact match gets points
- `energy` - compared to the user's target energy
- `acousticness` - small bonus for acoustic songs if `likes_acoustic` is True, or for electronic songs if it's False

`Song` also has `tempo_bpm`, `valence` and `danceability`, but I'm not using them for now. When I looked at the data, tempo, danceability and acousticness go up and down almost together with energy, so adding all of them would basically count energy three or four times. Valence is the only one that actually behaves differently, so I might add it later.

**UserProfile stores:**

- `favorite_genre`
- `favorite_mood`
- `target_energy` (from 0 to 1)
- `likes_acoustic` (True / False)

**The taste profile I test with** (in `src/main.py`):

```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,
}
```

This is a late-night study listener. I picked it because the catalog has three lofi songs, so genre alone can't decide the order and mood and energy have to do real work. It should also be easy to tell apart from "intense rock": Storm Runner has the wrong genre, the wrong mood, energy 0.91 and almost no acoustic sound, so it should end up near the bottom of the list.

**Algorithm recipe** (max score is 5.0):

1. Score every song in the catalog. There are no hard filters, so a song with the wrong genre can still win if everything else fits.
2. **Genre:** +1.5 for an exact match, +0.75 for a partial match ("pop" and "indie pop").
3. **Mood:** +1.5 for an exact match.
4. **Energy:** up to +1.5 using `1.5 * (1 - abs(song.energy - target_energy))`.
5. **Acousticness:** up to +0.5. If `likes_acoustic` is True the song gets `0.5 * acousticness`, otherwise `0.5 * (1 - acousticness)`.
6. Sort from highest to lowest score (ties keep the CSV order) and return the top k. The explanation lists which rules gave the song points.

**Advanced features (Challenge 1):** songs also have `popularity`, `release_decade`, `mood_tags`, `instrumentalness` and `explicit`. Each new rule only counts if the profile sets that preference, so my three main profiles still score out of 5.0 exactly like before.

- **Mood tags:** +0.5 for each tag the song shares with the profile's `mood_tags`, up to +1.0. This gives credit for moods that are close but not the same word, like an "euphoric" song tagged "uplifting" for a happy listener.
- **Decade:** +0.5 for the `favorite_decade`, +0.25 for the decade right next to it.
- **Popularity:** up to +0.5 for being close to `target_popularity` (0-100).
- **Instrumental:** up to +0.5, works like the acoustic rule, based on `likes_instrumental`.
- **Explicit:** -1.0 if `allow_explicit` is False and the song has explicit lyrics.

The score is shown out of the best possible score for that profile, so Family Road Trip (High-Energy Pop plus all the new preferences) is out of 7.5.

**Why genre and mood are worth the same:** my first plan was +2 for genre and +1 for mood. When I tested it on a few profiles, a "pop, happy" listener got Gym Hero (pop, intense) above Rooftop Lights (indie pop, happy), and a "pop, chill, low energy" listener got the energetic Sunrise City as the #2 pick. Genre is your long-term taste, but mood is what you want right now, so I made them equal. That put Rooftop Lights at #2 and pushed Sunrise City down to #4. I also tried making mood worth more than genre (1 and 2). It helped the "pop + chill" listener even more, but then a genre match was worth less than being 0.67 closer in energy, so I kept them equal.

**My plan (data flow):**

```mermaid
flowchart LR
    A["User prefs<br/>genre, mood, energy, acoustic"] --> C
    B["data/songs.csv"] --> L["load_songs<br/>strings to numbers"] --> C
    C["Loop: score_song on every song<br/>genre +1.5, mood +1.5,<br/>energy up to +1.5, acoustic up to +0.5"] --> D["Sort by score,<br/>highest first"]
    D --> E["Top k songs<br/>with reasons"]
```

For example, the row `4,Library Rain,...,lofi,chill,0.35,...,0.86` becomes a dict with `energy=0.35`, gets +1.5 (genre) +1.5 (mood) +1.42 (energy) +0.43 (acoustic) = 4.85 for my lofi listener, and ends up #1. The expected top 5 for that profile is Library Rain, Midnight Coding, Focus Flow, Spacewalk Thoughts and Coffee Shop Stories, so I can check my code against it.

**Biases I expect:**

- **Mood is exact-match only.** "relaxed", "peaceful" and "focused" get 0 points, the same as "sad" or "angry". So for my lofi listener the sad Empty Station Blues ranks above the peaceful Moonlit Nocturne, because only energy and acousticness are left to decide.
- **Genre can still beat what the user asked for.** A genre match alone is worth 1.5 points, and the energy rule is forgiving. A "pop, chill, low energy" listener still gets Gym Hero (energy 0.93) in their top 5.
- **Related genres don't count.** The partial match only works when one name contains the other ("pop" and "indie pop"). Lofi and ambient, or r&b and hip hop, are treated as completely unrelated.
- **Small, uneven catalog.** 15 of the 17 genres have only one song, so a metal or folk fan gets one real match and the rest of their top 5 is filled by energy alone. The catalog is also mostly Western genres.
- **Made-up numbers.** The values for songs 11-20 were estimated with AI, not measured, so they may carry stereotypes like "classical is always calm" or "metal is always angry".
- **One genre and one mood per user.** The profile can't describe someone with mixed taste.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main`, one block per profile. Every run starts with:

```text
$ python -m src.main
Loading songs from data/songs.csv...
Loaded songs: 20
```

### High-Energy Pop

```text
Top 5 for: High-Energy Pop
  pop / happy / energy 0.80 / prefers electronic
============================================================
 1. Sunrise City by Neon Echo                    4.88 / 5.00
      + genre match: pop (+1.50)
      + mood match: happy (+1.50)
      + energy 0.82 vs your 0.80 (+1.47)
      + acousticness 0.18 (+0.41)
------------------------------------------------------------
 2. Rooftop Lights by Indigo Parade              4.01 / 5.00
      + similar genre: indie pop (+0.75)
      + mood match: happy (+1.50)
      + energy 0.76 vs your 0.80 (+1.44)
      + acousticness 0.35 (+0.33)
------------------------------------------------------------
 3. Gym Hero by Max Pulse                        3.28 / 5.00
      + genre match: pop (+1.50)
      + energy 0.93 vs your 0.80 (+1.30)
      + acousticness 0.05 (+0.47)
------------------------------------------------------------
 4. Concrete Crown by Kilo Verse                 1.93 / 5.00
      + energy 0.78 vs your 0.80 (+1.47)
      + acousticness 0.08 (+0.46)
------------------------------------------------------------
 5. Fuego Lento by Ritmo Solar                   1.93 / 5.00
      + energy 0.80 vs your 0.80 (+1.50)
      + acousticness 0.15 (+0.42)
------------------------------------------------------------
```

### Chill Lofi

```text
Top 5 for: Chill Lofi
  lofi / chill / energy 0.40 / likes acoustic
============================================================
 1. Library Rain by Paper Lanterns               4.85 / 5.00
      + genre match: lofi (+1.50)
      + mood match: chill (+1.50)
      + energy 0.35 vs your 0.40 (+1.42)
      + acousticness 0.86 (+0.43)
------------------------------------------------------------
 2. Midnight Coding by LoRoom                    4.82 / 5.00
      + genre match: lofi (+1.50)
      + mood match: chill (+1.50)
      + energy 0.42 vs your 0.40 (+1.47)
      + acousticness 0.71 (+0.35)
------------------------------------------------------------
 3. Focus Flow by LoRoom                         3.39 / 5.00
      + genre match: lofi (+1.50)
      + energy 0.40 vs your 0.40 (+1.50)
      + acousticness 0.78 (+0.39)
------------------------------------------------------------
 4. Spacewalk Thoughts by Orbit Bloom            3.28 / 5.00
      + mood match: chill (+1.50)
      + energy 0.28 vs your 0.40 (+1.32)
      + acousticness 0.92 (+0.46)
------------------------------------------------------------
 5. Coffee Shop Stories by Slow Stereo           1.90 / 5.00
      + energy 0.37 vs your 0.40 (+1.46)
      + acousticness 0.89 (+0.45)
------------------------------------------------------------
```

### Deep Intense Rock

```text
Top 5 for: Deep Intense Rock
  rock / intense / energy 0.90 / prefers electronic
============================================================
 1. Storm Runner by Voltline                     4.93 / 5.00
      + genre match: rock (+1.50)
      + mood match: intense (+1.50)
      + energy 0.91 vs your 0.90 (+1.48)
      + acousticness 0.10 (+0.45)
------------------------------------------------------------
 2. Gym Hero by Max Pulse                        3.43 / 5.00
      + mood match: intense (+1.50)
      + energy 0.93 vs your 0.90 (+1.46)
      + acousticness 0.05 (+0.47)
------------------------------------------------------------
 3. Afterglow Rush by Pulse Theory               1.92 / 5.00
      + energy 0.95 vs your 0.90 (+1.43)
      + acousticness 0.02 (+0.49)
------------------------------------------------------------
 4. Iron Tide by Black Meridian                  1.88 / 5.00
      + energy 0.97 vs your 0.90 (+1.40)
      + acousticness 0.03 (+0.48)
------------------------------------------------------------
 5. Sunrise City by Neon Echo                    1.79 / 5.00
      + energy 0.82 vs your 0.90 (+1.38)
      + acousticness 0.18 (+0.41)
------------------------------------------------------------
```

### Family Road Trip

```text
Top 5 for: Family Road Trip
  pop / happy / energy 0.80 / prefers electronic
  mood tags: sunny, uplifting, warm
  decade: 2010s
  popularity: 80
  prefers vocals
  no explicit lyrics
============================================================
 1. Sunrise City by Neon Echo                    7.11 / 7.50
      + genre match: pop (+1.50)
      + mood match: happy (+1.50)
      + energy 0.82 vs your 0.80 (+1.47)
      + acousticness 0.18 (+0.41)
      + mood tags: uplifting, sunny (+1.00)
      + from the 2020s, next to your 2010s (+0.25)
      + popularity 82 vs your 80 (+0.49)
      + instrumentalness 0.02 (+0.49)
------------------------------------------------------------
 2. Rooftop Lights by Indigo Parade              6.42 / 7.50
      + similar genre: indie pop (+0.75)
      + mood match: happy (+1.50)
      + energy 0.76 vs your 0.80 (+1.44)
      + acousticness 0.35 (+0.33)
      + mood tags: uplifting, warm (+1.00)
      + from the 2010s (+0.50)
      + popularity 70 vs your 80 (+0.45)
      + instrumentalness 0.10 (+0.45)
------------------------------------------------------------
 3. Gym Hero by Max Pulse                        4.46 / 7.50
      + genre match: pop (+1.50)
      + energy 0.93 vs your 0.80 (+1.30)
      + acousticness 0.05 (+0.47)
      + from the 2020s, next to your 2010s (+0.25)
      + popularity 88 vs your 80 (+0.46)
      + instrumentalness 0.05 (+0.47)
------------------------------------------------------------
 4. Afterglow Rush by Pulse Theory               3.44 / 7.50
      + energy 0.95 vs your 0.80 (+1.28)
      + acousticness 0.02 (+0.49)
      + mood tags: uplifting (+0.50)
      + from the 2010s (+0.50)
      + popularity 85 vs your 80 (+0.47)
      + instrumentalness 0.60 (+0.20)
------------------------------------------------------------
 5. Island Time by Coastline Collective          3.31 / 7.50
      + energy 0.58 vs your 0.80 (+1.17)
      + acousticness 0.40 (+0.30)
      + mood tags: sunny, warm (+1.00)
      + popularity 57 vs your 80 (+0.39)
      + instrumentalness 0.08 (+0.46)
------------------------------------------------------------
```

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



