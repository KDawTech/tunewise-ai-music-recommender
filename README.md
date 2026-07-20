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

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
  Each song uses genre, mood, energy, tempo, valence, danceability, and acousticness.
- What information does your `UserProfile` store
It stores the user’s favorite genre, favorite mood, target energy level, and acoustic preference
- How does your `Recommender` compute a score for each song
It gives 2 points for a genre match, 1 point for a mood match, and up to 1 point for energy similarity
- How do you choose which songs to recommend
The system scores every song, sorts them from highest to lowest score, and returns the top five songs

You can include a simple diagram or bullet list if helpful.

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
User Profile: Intense Rock
Genre: rock | Mood: intense | Energy: 0.9

Recommendations:

1. Storm Runner by Voltline - Score: 3.99
   Because: genre match (+2.00), mood match (+1.00), energy similarity (+0.99)

2. Gym Hero by Max Pulse - Score: 1.97
   Because: mood match (+1.00), energy similarity (+0.97)

3. Sunrise City by Neon Echo - Score: 0.92
   Because: energy similarity (+0.92)

4. Rooftop Lights by Indigo Parade - Score: 0.86
   Because: energy similarity (+0.86)

5. Night Drive Loop by Neon Echo - Score: 0.85
   Because: energy similarity (+0.85)


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
I tested High-Energy Pop, Chill Lofi, and Intense Rock profiles. Each profile produced different recommendations based on its genre, mood, and energy preferences.
- What happened when you added tempo or valence to the score
Songs with a matching genre usually ranked highest because genre matches receive 2 points.
- How did your system behave for different types of users
Energy similarity helped rank songs even when the genre or mood did not match exactly

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

It only uses a small catalog of 10 songs, so the recommendations have limited variety.
It does not understand lyrics, language, listening history, playlists, likes, or skipped songs.

You will go deeper on this in your model card.


---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
I learned that recommender systems compare user preferences with item features and convert those matches into scores. The system then ranks the items by score and recommends the highest-ranked results.

- about where bias or unfairness could show up in systems like this
Bias can appear in the dataset or scoring rules. If some genres have more songs or receive more points, they may appear more often and reduce variety for users with different preferences



