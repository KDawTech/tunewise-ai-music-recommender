```markdown
# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MusicMatch 1.0**

---

## 2. Intended Use  

This recommender is designed to generate song recommendations based on a user’s preferred genre, mood, and energy level. It assumes that the preferences entered by the user accurately represent the type of music they want to hear. This model was created for classroom exploration and is not intended for real-world use.

---

## 3. How the Model Works  

The model uses each song’s genre, mood, and energy level to calculate a recommendation score. The user provides a preferred genre, preferred mood, and target energy level.

A song receives 2 points when its genre matches the user’s preferred genre. It receives 1 point when its mood matches the user’s preferred mood. It can also receive up to 1 point depending on how close its energy level is to the user’s target energy.

After every song is scored, the model sorts the songs from highest to lowest score and returns the top five recommendations. I changed the starter logic by adding CSV loading, score calculations, ranking, and explanations for each recommendation.

---

## 4. Data  

The model uses a catalog of 10 songs. The genres represented include pop, lofi, rock, ambient, jazz, synthwave, and indie pop. The moods represented include happy, chill, intense, relaxed, moody, and focused.

I did not add or remove songs from the starter dataset. The dataset is missing parts of musical taste such as lyrics, language, release year, favorite artists, listening history, likes, skipped songs, and playlist activity.

---

## 5. Strengths  

The system works well for users who have clear genre, mood, and energy preferences. It correctly ranks songs higher when they match the user’s preferred genre and mood while also having a similar energy level.

The recommendations matched my expectations during testing. The High-Energy Pop profile ranked pop songs highly, the Chill Lofi profile ranked lofi songs highly, and the Intense Rock profile ranked the rock song first.

---

## 6. Limitations and Bias  

The system does not consider lyrics, language, artists, listening history, tempo preferences, valence, danceability, or user feedback. Some genres and moods are underrepresented because they only appear once, while lofi and chill appear multiple times.

The system may favor genre too heavily because a genre match receives more points than mood or energy similarity. Users whose favorite genres appear more often in the dataset may receive more suitable and varied recommendations than users whose preferred genres are missing or underrepresented.

---

## 7. Evaluation  

I tested the recommender using three user profiles: High-Energy Pop, Chill Lofi, and Intense Rock. I checked whether songs with matching genres and moods ranked near the top and whether their energy levels were close to the user’s target.

I also used automated tests to confirm that the recommendations were sorted correctly and that each recommendation had a non-empty explanation. One surprising result was that songs without matching genres or moods could still rank reasonably well when their energy levels were close to the user’s target.

---

## 8. Future Work  

Future versions could include tempo, valence, danceability, acousticness, favorite artists, listening history, likes, and skipped songs in the scoring process. The recommendation explanations could also show a clearer breakdown of matching and nonmatching features.

Recommendation diversity could be improved by limiting repeated genres or artists in the top results. The model could also support multiple favorite genres and moods and allow users to choose how important each preference is.

---

## 9. Personal Reflection  

I learned that recommender systems compare user preferences with item features and use scoring rules to rank possible choices. I also learned that small changes in feature weights can significantly change the recommendation order.

It was interesting to see how a simple algorithm could still produce recommendations that felt personalized. This project changed how I think about music recommendation apps because real applications likely use much larger datasets, more user behavior, and more advanced algorithms.
```

