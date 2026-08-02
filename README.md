# TuneWise: AI-Powered Music Recommendation System

TuneWise recommends songs based on a user’s preferred genre, mood, energy level, and acoustic preference. It retrieves and ranks songs from a verified local catalog, then uses Groq AI to rewrite verified recommendation reasons into natural language.

## Original Project

TuneWise extends **Project 3: Music Recommender Simulation**.

The original project loaded songs from a CSV file, scored them using genre, mood, and energy similarity, and displayed the top recommendations in the terminal.

Project 4 adds:

- Streamlit web interface
- Acoustic preference scoring
- Groq-generated explanations
- Input and output guardrails
- Rule-based fallback behavior
- Interaction logging
- Automated and human reliability testing

## How the System Works

1. The user selects music preferences in Streamlit.
2. Input guardrails validate the preferences.
3. Songs are loaded from `data/songs.csv`.
4. The deterministic recommender scores and ranks every song.
5. The top-ranked songs are sent to Groq with verified explanations.
6. Output guardrails remove unknown or duplicate song IDs.
7. Results are displayed and recorded in a structured log.
8. If Groq fails, rule-based explanations are used.

The Mermaid architecture source is located at:

```text
diagrams/architecture.md
```

## Scoring System

Each song can receive:

- `2.0` points for matching genre
- `1.0` point for matching mood
- Up to `1.0` point for energy similarity
- Up to `1.0` point for acoustic preference similarity

The maximum score is `5.0`.

The displayed match percentage is calculated as:

```text
score / 5.0 × 100
```

This percentage is a rule-based similarity score, not a statistical probability.

## Project Structure

```text
tunewise-ai-music-recommender/
├── app.py
├── README.md
├── model_card.md
├── evaluation_results.md
├── requirements.txt
├── pytest.ini
├── data/
│   └── songs.csv
├── diagrams/
│   └── architecture.md
├── logs/
├── src/
│   ├── ai_service.py
│   ├── guardrails.py
│   ├── logger.py
│   ├── main.py
│   └── recommender.py
└── tests/
    ├── test_guardrails.py
    └── test_recommender.py
```

## Setup Instructions

### 1. Clone the repository

```powershell
git clone https://github.com/KDawTech/tunewise-ai-music-recommender.git
cd tunewise-ai-music-recommender
```

### 2. Create a virtual environment

```powershell
python -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 5. Create a `.env` file

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-20b
```

The `.env` file must not be committed to GitHub.

TuneWise still works without an API key by using rule-based explanations.

### 6. Run the application

```powershell
streamlit run app.py
```

## Sample Interaction 1

### Input

```text
Genre: ambient
Mood: chill
Energy: 0.70
Prefer acoustic music: No
Recommendations: 5
```

### Output

```text
1. Spacewalk Thoughts — Orbit Bloom
   Match: 73%
   Why it fits: Genre match, mood match, weak energy similarity,
   and the song is more acoustic than preferred.
```

## Sample Interaction 2

### Input

```text
Genre: pop
Mood: happy
Energy: 0.80
Prefer acoustic music: No
Recommendations: 5
```

### Output

```text
1. Sunrise City — Neon Echo
   Match: approximately 96%
   Why it fits: Genre match, mood match, strong energy similarity,
   and strong less-acoustic preference match.
```

## Sample Interaction 3

### Input

```text
Genre: lofi
Mood: chill
Energy: 0.35
Prefer acoustic music: Yes
Recommendations: 5
```

### Output

```text
1. Library Rain — Paper Lanterns
2. Midnight Coding — LoRoom
3. Focus Flow — LoRoom
```

## Guardrails

TuneWise validates that:

- Genre and mood are provided
- Energy is between `0.0` and `1.0`
- Recommendation count is between 1 and 10
- AI responses contain only retrieved song IDs
- Duplicate and unknown song IDs are removed
- Missing explanations use deterministic fallback text

The AI does not select songs or change their ranking.

## Testing

Run all tests with:

```powershell
python -m pytest -q
```

The automated tests check:

- Recommendation ordering
- Non-empty explanations
- Preference normalization
- Invalid energy rejection
- Fabricated song-ID removal
- Duplicate song-ID removal

Human evaluation results are documented in:

```text
evaluation_results.md
```

## Testing Summary

The initial AI explanation test failed because the model described energy `0.28` as close to a requested value of `0.70`. It also described acousticness `0.92` as not overly acoustic.

The prompt was changed so that the AI may only rewrite verified rule-based reasons. After the change, the explanation correctly reported weak energy similarity and that the song was more acoustic than preferred.

## Design Decisions

The recommendation ranking is deterministic so that results are reproducible and testable.

Groq is used only to improve explanation wording. It cannot add songs, change scores, or change the ranking.

The local CSV catalog prevents the application from displaying invented songs. A fallback system ensures TuneWise remains functional when the AI service is unavailable.

## Limitations

- The catalog contains only 10 fictional songs.
- Genre and mood use exact matching.
- Scoring weights are manually selected.
- The system does not learn from listening history.
- It does not analyze audio or lyrics.
- Match percentages are not calibrated probabilities.
- Recommendations may have limited variety.

## Reflection

This project taught me that adding an AI API does not automatically make a system reliable. The application also needs deterministic logic, validated inputs, controlled context, output checks, fallback behavior, logging, and testing.

The inaccurate first AI explanation showed that model output can sound confident while contradicting the data. Restricting the AI to verified evidence made TuneWise more accurate, transparent, and responsible.

See `model_card.md` for additional reflection, limitations, bias, ethics, and AI collaboration details.



