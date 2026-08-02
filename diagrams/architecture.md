# TuneWise System Architecture

```mermaid
flowchart TD
    A[User] --> B[Streamlit Interface]

    B --> C[Preference Guardrails]
    C -->|Valid input| D[Local Song Catalog]
    C -->|Invalid input| E[Display Validation Error]

    D --> F[Deterministic Retriever and Ranker]
    F --> G[Top-K Retrieved Songs]

    G --> H{Groq API Available?}

    H -->|Yes| I[Groq Explanation Generator]
    I --> J[Output Guardrails]
    J -->|Valid song IDs only| K[Grounded Explanations]
    J -->|Missing or invalid output| L[Rule-Based Fallback]

    H -->|No| L

    K --> M[Streamlit Results]
    L --> M

    M --> N[Structured Interaction Logger]
    M --> O[Human Evaluation]

    P[Pytest Reliability Suite] --> C
    P --> F
    P --> J