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

Before this project I thought Spotify just looked at what genre I listen to. It turns out real platforms mix two ideas. Collaborative filtering looks at what other people with a similar listening history play, skip and add to playlists, so it can suggest songs I would never find on my own. Content-based filtering looks at the song itself (genre, tempo, energy, how "happy" it sounds) and finds tracks that are similar to the ones I already like. Spotify and YouTube use both at the same time, plus a lot of behavior data like skips and watch time. My simulation only has a CSV with 10 songs and no data about other users, so I'm building a content-based recommender. It will prioritize genre first, then mood, and then how close the song's energy is to what the user wants. I care about "close to" and not "higher", because if someone wants chill music, the most energetic song in the list is the worst pick for them, not the best.

**Song features I use in the score:**

- `genre` - exact match gets the most points, a partial match like "pop" and "indie pop" gets half
- `mood` - match gets points
- `energy` - compared to the user's target energy
- `acousticness` - small bonus or penalty depending on `likes_acoustic`

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

**How a song gets its score:** +2 for a genre match (+1 if it's only partial), +1 for a mood match, up to +1.5 for energy using `1.5 * (1 - abs(song.energy - target_energy))`, and up to +0.5 for the acoustic preference. Then I sort all songs from highest to lowest score and return the top k.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

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



