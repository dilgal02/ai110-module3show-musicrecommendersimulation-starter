# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeJudge 1.0**

I called it that because it works like a judge. It gives every song points and the songs with the most points win.

---

## 2. Intended Use  

**Goal / task:** VibeJudge suggests 5 songs out of a list of 20 that fit what one listener wants right now. It doesn't learn from your listening history. It only compares each song to four things you tell it: your favorite genre, your mood, how much energy you want, and if you like acoustic music.

**What it assumes about you:** you have one favorite genre and one mood, you can say your energy as a number from 0 to 1, and you type the genre and mood exactly like they are written in the song list.

**Intended use:** this is a classroom project. It's for learning how a recommender turns data into points and a ranked list, and for trying out different listeners to see why songs get picked.

**Not intended for:**

- Real people choosing real music. The catalog is tiny and the songs are made up.
- Anything where the result matters, like deciding which artists get promoted or paid.
- Listeners with mixed taste, like someone who loves both jazz and metal. The system only understands one genre and one mood.
- Learning facts about real genres. The numbers for half of the songs were guessed by AI.

---

## 3. How the Model Works  

The recommender works like a judge handing out points. It looks at every song in the catalog, one at a time, and gives it points for how well it fits what the listener asked for. Then it lines the songs up from most points to fewest and shows the top five.

**What it knows about each song:** its genre (like pop or lofi), its mood (like happy or chill), its energy (how calm or intense it feels, from 0 to 1) and its acousticness (how much it sounds like real instruments instead of electronic sounds).

**What it knows about the listener:** their favorite genre, the mood they want, how much energy they want, and whether they like acoustic music.

**How the points work** (a perfect song gets 5 points):

- **Genre:** 1.5 points if it's the listener's favorite genre, and half of that if the name is a close relative, like "indie pop" for a pop fan.
- **Mood:** 1.5 points if the mood matches.
- **Energy:** up to 1.5 points. A song gets all 1.5 when its energy is exactly what the listener wants, and fewer the further away it is. It's about being close, not about being high: for someone who wants calm music, the most intense song is the worst pick, not the best.
- **Acoustic sound:** up to 0.5 points. If the listener likes acoustic music, more acoustic songs get more points. If not, more electronic songs do. This is a small tiebreaker.

Every song also gets a short list of reasons, like "mood match: chill (+1.50)", so the listener can see exactly why it was picked.

**Extra rules (optional):** a listener can also pick mood tags (like "sunny" or "cozy"), a favorite decade, how popular they want the songs to be, if they like songs without singing, and if explicit lyrics are okay. Each of these adds a small bonus, or takes away a point for explicit songs, but only if the listener actually set it.

**Example:** my late-night study listener wants lofi, a chill mood, low energy and acoustic sound. "Library Rain" matches the genre and the mood, has almost exactly the right energy and sounds very acoustic, so it gets 4.85 out of 5 and comes first. "Storm Runner" is a loud rock song that matches none of that, so it gets 0.79 and lands near the bottom.

**What I changed from the starter logic:** the usual starting point gives 2 points for genre and 1 for mood. When I tested that, a "happy pop" listener got an intense gym song as their #2 pick, ahead of a happy indie pop song, just because genre was worth twice as much as mood. I think the genre you usually like and the mood you're in right now matter about the same, so I made them equal. I also left out tempo and danceability, because they mostly rise and fall together with energy, so adding them would count energy two or three times. Valence (how happy a song sounds) behaves differently, so I might add it later.

---

## 4. Data  

- The catalog has **20 songs** in `data/songs.csv`. The starter file had 10, and I added 10 more with AI help so there would be new genres and moods.
- Every song has a title, artist, genre, mood, energy, tempo, valence, danceability and acousticness. For Challenge 1 I added 5 more: popularity (0 to 100), release decade, a few mood tags, instrumentalness, and if it has explicit lyrics. The main scoring uses **genre, mood, energy and acousticness**. The new ones only count if a listener asks for them.
- There are 17 genres and 16 moods. But 15 of the genres and 13 of the moods have only **one song**. Only lofi (3 songs) and pop (2 songs) have more than one.
- All songs and artists are made up. The numbers for songs 11 to 20, and all of the new Challenge 1 columns, were guessed by AI, not measured from real audio.
- What's missing:
  - No songs that are acoustic and energetic at the same time, and only 2 that are calm and electronic.
  - No songs with energy between 0.58 and 0.75.
  - Mostly Western genres, so no k-pop, afrobeats, bollywood and so on.
  - No lyrics, language, popularity or listening history at all.

---

## 5. Strengths  

- It works well for "typical" listeners whose genre and mood are in the catalog. Happy pop, chill lofi and intense rock all got the obvious #1 song, the one that matches everything they asked for.
- It tells opposite listeners apart really easily. The chill lofi and intense rock lists have zero songs in common.
- Energy is about being close, not about being high. So a calm listener doesn't get loud songs just because they have "more" energy.
- Every song comes with its reasons and points, so you can always see why it got picked. This made it easy to find the bugs.
- It's pretty stable. Even when I doubled the energy weight, the #1 songs mostly stayed the same and only songs that were almost tied swapped places.

---

## 6. Limitations and Bias 

The system quietly assumes that calm music is acoustic and energetic music is electronic. My 20-song catalog has 9 calm acoustic songs and 9 energetic electronic songs, but zero songs that are both acoustic and energetic, and only 2 that are calm and electronic. So a listener who wants upbeat acoustic music, like a lively folk or country fan, can never get a song that fits both wishes: when I tested every combination of genre, mood, energy and acoustic preference (2,720 simulated listeners), 82% of high-energy acoustic listeners got a #1 song that scored under 60% of the maximum, compared to 17% of medium-energy acoustic listeners. The scoring math treats everyone the same, but because the data is lopsided, these listeners are effectively ignored. Adding songs that break this pattern, or turning the acoustic preference into a target number instead of a yes/no, would help.

---

## 7. Evaluation  

**Profiles I tested**

I made three main listeners and ran the program for each one, and later added a fourth one for Challenge 1:

- **High-Energy Pop:** likes pop, wants happy songs, wants high energy (0.8), doesn't care about acoustic stuff.
- **Chill Lofi:** likes lofi, wants chill songs, wants low energy (0.4), likes acoustic. This is basically me studying at night.
- **Deep Intense Rock:** likes rock, wants intense songs, wants very high energy (0.9), doesn't like acoustic.
- **Family Road Trip:** the same as High-Energy Pop, plus mood tags (sunny, uplifting, warm), the 2010s, popularity around 80, songs with singing, and no explicit lyrics. It keeps the same top 3 as High-Energy Pop, but the explicit Concrete Crown and Fuego Lento drop out, and two songs tagged "sunny" or "uplifting" come in.

Then I tried some weird "trick" listeners to see if I could break it: a pop fan who wants sad songs but also high energy, a k-pop fan (there is no k-pop in my list), the happy pop listener typed with extra spaces, an energy of 5 (it's supposed to be 0 to 1), and the word "False" typed as text. Two tries made the program crash completely: giving it two genres at once, and typing the energy as text instead of a number.

For every listener I looked at the top 5 and asked myself "would this person actually want these songs?"

**Comparing the profiles**

- **High-Energy Pop vs Chill Lofi:** they have zero songs in common. The pop list is all loud, electronic songs (energy 0.76 to 0.93) and the lofi list is all quiet, acoustic songs (energy 0.28 to 0.42). That makes sense, because these two people want the opposite thing on pretty much everything.
- **Chill Lofi vs Deep Intense Rock:** also zero songs in common. Storm Runner is #1 for the rock fan but #17 out of 20 for the lofi listener, and Library Rain is the exact other way around (#1 for lofi, #17 for rock). This is good. It means the system can tell "chill lofi" and "intense rock" apart really easily.
- **High-Energy Pop vs Deep Intense Rock:** these two share two songs, Gym Hero and Sunrise City. That kind of makes sense, because both people want loud electronic music, they just want a different genre and mood. But the rock list gets weird after #2. There is only one rock song in my whole catalog, so spots 3 to 5 are just "whatever is loud", and Iron Tide (metal) ends up below Afterglow Rush (EDM), even though metal is way closer to rock. The system has no idea that metal and rock are kind of the same family.
- **High-Energy Pop vs the same listener with typos:** I typed "Pop " and "Happy " with a space at the end. Sunrise City went from 4.88 points to 2.63, and Rooftop Lights fell out of the top 5 completely. One tiny space and the system thinks this person isn't a happy pop fan anymore.
- **High-Energy Pop vs the sad pop fan:** I changed the mood from happy to sad and the energy to 0.9. The top 2 are still Gym Hero and Sunrise City, which are not sad at all. The only sad song (Empty Station Blues) is #3, because it's slow and the person asked for fast. So when the mood and the energy fight, the energy and the "pop" label win.

**Why does Gym Hero keep showing up for Happy Pop?**

Gym Hero is #3 for the happy pop listener, even though it's a workout song and its mood is "intense", not happy. It still gets points for three things: it has the "pop" label (1.5 points), it's loud like the person wants (1.3 points), and it sounds very electronic (almost 0.5 points). It gets nothing for mood, but that still adds up to 3.28. There are only two pop songs in the whole catalog, so it doesn't have much competition. Basically the system sees the "pop" sticker and gives it points without checking if the song actually sounds happy. With my first idea (genre worth 2 points and mood worth 1) it was even #2, above Rooftop Lights, which actually is a happy song. That's why I made genre and mood worth the same.

**What surprised me**

- The #1 song for Chill Lofi is decided by a really small thing. Library Rain beats Midnight Coding by only 0.03 points, just because it sounds a little more acoustic. If I make the acoustic part a bit smaller, they switch places.
- When I doubled how much energy counts and cut genre in half, the top songs barely changed. It mostly just swapped songs that were already almost tied. So the results got different, not better.
- I thought pop songs would get recommended the most, but it's actually the calm acoustic ones. When I tested every possible listener, Spacewalk Thoughts and Paper Boats showed up in 42% of all top 5 lists, and Iron Tide in only 14%. When the system can't find your genre or mood, it just falls back to energy and acoustic sound, and those two songs fit "in the middle" of a lot of people.
- Typing "False" as text counts as yes, so someone who doesn't want acoustic music gets acoustic songs anyway. And an energy of 5 makes every single score negative.

---

## 8. Future Work  

1. **Give points for similar moods and genres.** Right now "relaxed" gets zero points for a "chill" listener, and metal gets zero for a rock fan. I'd give half points for related ones.
2. **Add more and different songs.** At least 3 songs per genre, plus songs that break the "calm = acoustic" pattern, like energetic acoustic songs and calm electronic songs.
3. **Check what the user types.** Remove extra spaces, keep energy between 0 and 1, and turn text like "False" or "0.9" into real values, so the program doesn't crash or give weird negative scores.

---

## 9. Personal Reflection  

**My biggest learning moment**

My biggest learning moment was finding out that the data matters more than the formula. My scoring rules treat every listener the same way, and there is no bug in the code. But my song list has zero songs that are both energetic and acoustic. So when I tried a listener who wants upbeat acoustic music, like a lively folk fan, they just got bad matches most of the time. Nothing in the code looks wrong, and it's still unfair to those people. I didn't expect a recommender to be biased without anybody writing anything biased.

**How AI helped, and when I had to double-check it**

AI helped me a lot with the typing. It added the 10 new songs to the CSV, wrote the first versions of the loading, scoring and ranking functions, and explained the difference between `sort()` and `sorted()` to me. I asked it to explain every step to me in Russian, so I actually understood what each part does and didn't just copy it. I also used a separate chat just for evaluation, and it came up with trick profiles I would never think of, like a space at the end of "Pop " or the word "False" typed as text.

But it was wrong more than once, so I learned to always make it check things by running the real code:

- At first it told me to run the program from inside the `src` folder. That broke as soon as the program started reading the CSV, and the README command `python -m src.main` didn't work either until the import was fixed.
- It wrote in my README that 14 of the 17 genres have only one song. When it recounted with code, the real number was 15.
- My README example said a song gets +1.43 for energy, but the program printed +1.42, so the example didn't add up to the total.
- The first version of the reasons said "acoustic sound" even for a loud rock song.
- The evaluation chat worked out its results by hand, so every profile got run through the real program to make sure. That time it was right.
- The numbers for the 10 new songs are AI guesses and I can't check them, so I wrote that down as a limitation instead of pretending they're real.

**What surprised me about simple algorithms**

My recommender is just four rules and adding up points. There is no machine learning at all. But when I ran it, the Chill Lofi list honestly looked like a real study playlist. I think what makes it feel real is the "reasons" under every song, because it explains itself like a real app would. Even its mistakes felt real: Gym Hero showing up for a happy pop fan is exactly the kind of weird pick I sometimes get on Spotify.

**What I would try next**

- Give half points for moods and genres that are close, like chill and relaxed, or rock and metal.
- Add more songs, especially ones that break the "calm = acoustic" pattern.
- Clean up what the user types, so extra spaces or numbers typed as text don't break it.
- Try adding valence, because it's the one feature that doesn't just copy energy.
