# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

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

**Example:** my late-night study listener wants lofi, a chill mood, low energy and acoustic sound. "Library Rain" matches the genre and the mood, has almost exactly the right energy and sounds very acoustic, so it gets 4.85 out of 5 and comes first. "Storm Runner" is a loud rock song that matches none of that, so it gets 0.79 and lands near the bottom.

**What I changed from the starter logic:** the usual starting point gives 2 points for genre and 1 for mood. When I tested that, a "happy pop" listener got an intense gym song as their #2 pick, ahead of a happy indie pop song, just because genre was worth twice as much as mood. I think the genre you usually like and the mood you're in right now matter about the same, so I made them equal. I also left out tempo and danceability, because they mostly rise and fall together with energy, so adding them would count energy two or three times. Valence (how happy a song sounds) behaves differently, so I might add it later.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
