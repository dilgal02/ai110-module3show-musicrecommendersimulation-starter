# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

Challenge 1: add 5 advanced song features to `data/songs.csv` and make the scoring in `src/recommender.py` use them, without breaking the profiles I already had.

**Prompts used:**

> Challenge 1: add advanced song features. Attached: @data/songs.csv, @src/recommender.py, @src/main.py. Add 5 new columns to songs.csv for all 20 songs: `popularity` (0-100), `release_decade` (e.g. 1990), `mood_tags` (2-3 detailed tags separated by '|', reusing tags across songs so they can match), `instrumentalness` (0-1) and `explicit` (true/false). Update `load_songs` to convert them, and add scoring rules in `score_song`: +0.5 per shared mood tag (max 2), +0.5 for the favorite decade (+0.25 for a neighboring one), up to +0.5 for popularity closeness, up to +0.5 for instrumental preference, and -1.0 for explicit songs when `allow_explicit` is False. Every new rule must be optional, so profiles that don't set the new preferences score exactly the same as before. Show each rule in the reasons, show the score out of the profile's real maximum, add one new profile that uses all the new preferences, and verify by running the code.

**What did the agent generate or change?**

- `data/songs.csv`: 5 new columns for all 20 songs (`popularity`, `release_decade`, `mood_tags`, `instrumentalness`, `explicit`). The tags reuse the same small set of words (calm, cozy, uplifting, warm, driving...) so songs can actually match each other.
- `src/recommender.py`:
  - `load_songs` converts the new columns: numbers to int or float, "true"/"false" to a real True/False, and "calm|cozy|rainy" to a list.
  - `score_song` has 5 new rules, and each one is skipped if the profile doesn't set that preference:

    | Feature | Rule | Max |
    |---|---|---|
    | mood tags | +0.5 per shared tag, up to 2 tags | +1.0 |
    | release decade | +0.5 same decade, +0.25 the decade next to it | +0.5 |
    | popularity | closer to the target popularity = more points | +0.5 |
    | instrumentalness | like the acoustic rule, based on `likes_instrumental` | +0.5 |
    | explicit | -1.0 if `allow_explicit` is False | penalty |

  - New `max_score(user_prefs)` function, so every profile is scored out of its own real maximum.
  - `Song` and `UserProfile` got the new fields with default values, so the old tests still work.
- `src/main.py`: new profile "Family Road Trip" (High-Energy Pop plus all the new preferences). The header now lists the extra preferences, and the score is shown out of the profile's max (7.50 for this one).

**What did you verify or fix manually?**

Checks after the change:

- The three old profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) print exactly the same output as before. The full output was compared before and after the change, character by character.
- The original 10 columns in `songs.csv` are exactly the same as in the last commit.
- For every profile and every song (80 checks), the score equals the sum of the points in the reasons, and no score goes above the profile's max.
- The explicit penalty works: Concrete Crown goes from 3.42 to 2.42 for Family Road Trip, and nothing happens for profiles that don't set `allow_explicit`.
- Both tests in `tests/test_recommender.py` still pass.

Things that needed a fix or human review:

- The first version of the decade reason said "from the 2020s (+0.25)" for a listener who asked for the 2010s. That looked like a bug even though the math was right, so it was changed to "from the 2020s, next to your 2010s (+0.25)".
- The new values (popularity, tags and so on) are AI guesses for made-up songs. There is no way to check them, so the model card says that.

What changed in the results: compared to High-Energy Pop, Family Road Trip keeps the same top 3. Concrete Crown (explicit) and Fuego Lento drop out, and Afterglow Rush ("euphoric", tagged "uplifting") and Island Time ("carefree", tagged "sunny" and "warm") come in. That's good, because before this, "euphoric" and "carefree" songs got zero mood points for a happy listener. But Gym Hero is still #3, and now it even gets extra points for being popular and recent. So the popularity rule can make popular songs even harder to beat.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

A simple Strategy pattern. Each scoring mode is a small `ScoringMode` object that holds how many points the genre, mood, energy and acoustic rules are worth. `score_song` gets the mode as a parameter and uses its numbers instead of fixed constants. There are four modes: Balanced (the default), Genre-First, Mood-First and Energy-Focused.

**How did AI help you brainstorm or implement it?**

Prompt I used:

> Attached: @src/recommender.py. I want to add multiple scoring modes (Balanced, Genre-First, Mood-First, Energy-Focused) that a user can switch between in main.py. Brainstorm 3-4 design options for this, including a simple Strategy pattern, and compare them: how much code changes when I add a new mode, how easy it is to break the existing scoring, and how readable it is for a beginner. Recommend one. Then implement it on a branch called experiment/mood-first, keep Balanced as the default so `python -m src.main` gives the same results as before, add a --mode flag to main.py, and verify every mode by running it.

The AI compared four options:

| Option | Adding a new mode | Risk of breaking scoring |
|---|---|---|
| `if mode == ...` chain inside `score_song` | edit `score_song` every time | high |
| one scoring function per mode | copy the whole function | high, the copies drift apart |
| **strategy objects with weights (chosen)** | **one line in `MODES`** | **low, the rules stay in one place** |
| abstract base class + subclass per mode | a new class every time | low, but overkill for 4 numbers |

It recommended the strategy objects, because all the rules stay in one `score_song` and a mode only says how much each rule is worth. Other ideas from the brainstorm that I kept:

- Keep Balanced as the default, so the old command gives the same results as before. This was checked: the output is identical except for the new "Scoring mode" line.
- Build the Balanced mode from the existing constants, so my recipe numbers only live in one place.
- Use a `--mode` flag, so switching modes doesn't mean editing the code.
- Try it on the branch `experiment/mood-first` first, and merge it back into main only after the checks passed.

Checks after the change: for every mode, every profile and every song (320 checks) the score equals the sum of the reasons and never goes above the max. A wrong mode name gives a clear error, and the tests still pass. Genre-First brings back the problem I found in Phase 2 (Gym Hero above Rooftop Lights for a happy pop fan, 3.78 vs 3.77), and Energy-Focused gives exactly the same numbers as my weight-shift experiment. So the modes really reproduce the experiments.

What the modes change:

- **Genre-First:** Gym Hero jumps to #2 for High-Energy Pop, just because it has the pop label.
- **Mood-First:** Spacewalk Thoughts (ambient, chill) beats Focus Flow (lofi, focused) for Chill Lofi.
- **Energy-Focused:** Midnight Coding takes #1 from Library Rain, because its energy is closer.

**How does the pattern appear in your final code?**

- `ScoringMode` and the `MODES` dictionary at the top of `src/recommender.py`.
- `score_song(user_prefs, song, mode)`, `recommend_songs(..., mode)` and `max_score(user_prefs, mode)` all take the mode as a parameter, with Balanced as the default.
- The `--mode` flag in `src/main.py`, for example `python -m src.main --mode mood-first`.
