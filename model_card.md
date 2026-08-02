# TuneWise Model Card

## System Name

**TuneWise: AI-Powered Music Recommendation System**

## Intended Use

TuneWise is an educational music recommendation application. It recommends songs from a small verified catalog based on genre, mood, energy, and acoustic preference.

It demonstrates deterministic ranking, AI-generated explanations, guardrails, fallback behavior, logging, and reliability testing.

## How It Works

TuneWise gives each song:

- 2 points for a genre match
- 1 point for a mood match
- Up to 1 point for energy similarity
- Up to 1 point for acoustic preference similarity

Songs are ranked by score. Groq AI then rewrites verified recommendation reasons into natural language.

The AI does not select songs or change the ranking.

## Data

TuneWise uses `data/songs.csv`, which contains 10 fictional songs.

Each song includes:

- Title
- Artist
- Genre
- Mood
- Energy
- Tempo
- Valence
- Danceability
- Acousticness

## Reliability and Guardrails

TuneWise validates user input and rejects invalid energy values.

AI output is checked so that:

- Unknown song IDs are removed
- Duplicate song IDs are removed
- Empty explanations are rejected
- Missing explanations use rule-based fallback text
- Only songs retrieved from the local catalog are displayed

If Groq is unavailable, TuneWise continues working with deterministic explanations.

## Testing Results

Automated tests check:

- Recommendation ordering
- Non-empty explanations
- Preference normalization
- Invalid energy rejection
- Fabricated song-ID removal
- Duplicate song-ID removal

A human evaluation discovered that the first AI prompt produced an inaccurate explanation. It described energy `0.28` as close to `0.70` and described acousticness `0.92` as not overly acoustic.

The prompt was revised so that the AI may only rewrite verified reasons produced by the deterministic recommendation system.

After the revision, the explanation correctly reported:

- Weak energy similarity
- More acoustic than preferred

## Strengths

- Transparent scoring rules
- Reproducible recommendation ranking
- Verified local catalog
- Protection against invented songs
- Works without an AI API
- Automated and human evaluation
- Clear explanations for users

## Limitations

- The catalog contains only 10 fictional songs
- Genre and mood use exact matching
- Feature weights are manually selected
- The system does not learn from listening history
- It does not analyze lyrics or audio
- Recommendations may have limited variety
- Match percentages are not statistical probabilities
- AI wording may vary between runs

## Bias and Fairness

The catalog does not represent all genres, cultures, languages, or artists.

Some genres and moods appear more often than others. Users whose preferences appear frequently in the catalog may receive more suitable recommendations.

Genre also receives more weight than mood, which may favor exact genre matches.

## Ethical Considerations

TuneWise should not be used to make conclusions about a user’s personality, mental health, identity, or emotions.

The application should clearly explain that its results come from a small fictional catalog and manually selected scoring rules.

## AI Collaboration Reflection

AI assistance helped with planning the architecture, creating guardrails, building the Streamlit interface, writing tests, and organizing documentation.

One AI-generated explanation was flawed because it contradicted the actual song data. I identified the problem by comparing the explanation with the energy and acousticness values.

I did not accept the result automatically. I revised the prompt and system design so that the language model could only rewrite verified deterministic reasons.

This showed me that AI output must be reviewed and tested instead of trusted without verification.

## What I Learned

I learned that a reliable AI application requires more than calling a language model.

It also needs:

- Deterministic logic
- Input validation
- Controlled context
- Output validation
- Fallback behavior
- Logging
- Automated tests
- Human evaluation

Separating recommendation ranking from AI explanation generation made TuneWise easier to test, explain, and improve.

## Future Improvements

Future versions could include:

- A larger and more balanced catalog
- Multiple favorite genres and moods
- Adjustable scoring weights
- Favorite artist preferences
- Listening history and user feedback
- Recommendation diversity controls
- Spotify or another music-data integration
- Embedding-based semantic retrieval