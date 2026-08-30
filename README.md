# ✦ LearnPath AI — Editorial Learning Path & Mentor Studio

LearnPath AI is an intelligent, context-aware learning management and roadmap generator built with **Streamlit**, **NetworkX**, and **OpenAI GPT-4o**. It calculates technical skill gaps, visualizes dependency graphs for targeted career tracks, tracks course progress, and provides an active AI mentor tailored to your current learning trajectory.

---

## ⚡ Key Features

- ** Adaptive Baseline Profile:** Define target career tracks (AI/ML Engineer, Full-Stack Web Developer, Data Scientist, etc.), weekly study availability, and technical background.
- ** Skill Gap Diagnostics:** Automatically analyzes missing prerequisites and core requirements based on your target role.
- ** Dynamic Roadmap & Dependency Graph:** Uses `NetworkX` and `Matplotlib` to visualize skill dependency trees and track completed versus pending milestones.
- ** Curated Vault & Resources:** Recommends targeted courses and projects dynamically filtered by pending skills.
- ** Progress Tracking:** Complete interactive checklists with automatic state persistence (`user_state.json`).
- ** Context-Aware AI Mentor:** Integrated OpenAI assistant (`gpt-4o-mini`) connected directly to your profile metrics, completed skills, and active roadmap gaps.

---

## Project Structure

```text
learn-ai/
├── .streamlit/
│   ├── config.toml        # Custom editorial styling & theme configuration
│   └── secrets.toml       # API Key configuration (Git ignored)
├── data/
│   ├── courses.csv        # Course directory catalog
│   └── resources.csv      # Project & reading resources
├── modules/
│   ├── __init__.py
│   ├── ai_assistant.py    # OpenAI integration & context prompt engine
│   ├── persistence.py     # JSON state save/load utilities
│   ├── profile.py         # Profile baseline logic
│   ├── resources.py       # Data frame loader & resource filter
│   ├── roadmap.py         # Graph routing & roadmap generator
│   └── skill_gap.py       # Diagnostic engine
├── .gitignore             # Secrets & environment exclusions
├── app.py                 # Streamlit UI application router
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation
```

## Prerequisites
```
Python 3.9+ installed
Git installed
```

## Install Dependencies
```
(Bash)
pip install -r requirements.txt
```

## Tech Stack
1. Frontend / UI: Streamlit
2. Data Manipulation: Pandas
3. Graph & Visualization: NetworkX, Matplotlib
4. AI Integration: OpenAI API






