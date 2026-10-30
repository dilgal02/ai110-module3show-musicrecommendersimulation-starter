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

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
