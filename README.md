# AI-Based Interview Preparation Assistant Using Machine Learning and NLP

## 1. Project Title
**AI-Based Interview Preparation Assistant Using Machine Learning and NLP**

## 2. Abstract
Technical interview preparation is a critical but often unstructured part of a student's
placement journey. This project presents a Streamlit-based web application that helps
B.Tech students prepare for technical interviews by analyzing their resume, selecting
relevant interview questions by category and difficulty, and automatically evaluating
their written answers using Natural Language Processing (NLP) and Machine Learning (ML)
techniques — specifically TF-IDF vectorization and Cosine Similarity — combined with
rule-based keyword matching. The system stores all interview history in a local SQLite
database and presents a performance dashboard with weak-topic identification and
personalized study recommendations.

## 3. Problem Statement
Most students prepare for interviews using static question banks (PDFs, books, or
websites) with no way to objectively evaluate the quality of their own spoken/written
answers. There is no feedback loop: students cannot tell whether their answer covers the
key concepts an interviewer expects, nor can they track which topics they are
consistently weak in over time. This project addresses that gap with an automated,
NLP/ML-based answer evaluation and performance-tracking system.

## 4. Objectives
- Build a working end-to-end interview preparation web application.
- Extract text and technical skills from a student's uploaded resume.
- Provide a categorized, difficulty-tiered bank of interview questions.
- Evaluate free-text answers using TF-IDF + Cosine Similarity (NLP/ML) and keyword
  matching (rule-based).
- Provide numeric scores and human-readable feedback for every answer.
- Track performance over time and identify weak topics.
- Recommend focused study areas based on historical performance.

## 5. Features
1. Home / Dashboard with project-wide statistics
2. Student profile creation and management
3. Resume PDF upload
4. Resume text extraction (PyPDF2)
5. Rule-based skill extraction from resume text
6. Interview category selection (10 categories)
7. Difficulty selection: Easy / Medium / Hard
8. Randomized question selection from a 100-question dataset
9. Free-text answer submission
10. NLP-based answer evaluation
11. TF-IDF based text representation
12. Cosine similarity for semantic answer comparison
13. Keyword/concept matching (rule-based)
14. Final blended answer score
15. Detailed, human-readable feedback per answer
16. Weak-topic identification
17. Performance dashboard with charts (Plotly)
18. Interview history log
19. SQLite database persistence
20. Clean, responsive Streamlit UI with sidebar navigation
21. Error handling for missing files, invalid PDFs, empty answers, DB errors
22. Input validation on all forms

## 6. Technology Stack
| Layer | Technology |
|---|---|
| UI / Frontend | Streamlit |
| Language | Python 3.9+ |
| Data handling | Pandas, NumPy |
| ML / NLP | Scikit-learn (TF-IDF, Cosine Similarity), NLTK (tokenization, stop-words, lemmatization) |
| PDF parsing | PyPDF2 |
| Database | SQLite (built-in `sqlite3`) |
| Visualization | Plotly Express |

## 7. System Requirements
- Python 3.9 or higher
- pip package manager
- ~200 MB free disk space (for NLTK corpora + dependencies)
- Internet access on first run (to download NLTK data — the app also has a
  **fallback mode** that works fully offline if NLTK data cannot be downloaded)

## 8. Installation
```bash
# 1. Clone / copy the project folder
cd AI-Interview-Assistant

# 2. (Recommended) create a virtual environment
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## 9. How to Run
```bash
streamlit run app.py
```
This opens the application in your default browser at `http://localhost:8501`.

**First-run note:** on first launch, the app downloads a small NLTK dataset
(punkt, stopwords, wordnet) for tokenization and lemmatization. If you have no
internet access at that moment, the app automatically switches to a lightweight
regex-based fallback tokenizer so the application still works end-to-end.

## 10. Project Structure
```
AI-Interview-Assistant/
│
├── app.py                       # Main Streamlit application (all pages)
├── requirements.txt
├── README.md
├── .gitignore                   # Keeps venv/, __pycache__/, *.db out of git
├── vercel.json                  # Vercel config (static landing page build)
├── .vercelignore                # Keeps venv/ etc. out of the Vercel upload
├── public/
│   └── index.html               # Vercel landing page (links to live app + repo)
├── database/
│   └── database.py              # SQLite schema + CRUD operations
├── data/
│   └── interview_questions.csv  # 100-question dataset
├── models/
│   └── model.py                 # TF-IDF + Cosine Similarity model wrapper
├── modules/
│   ├── resume_analyzer.py       # PDF text extraction + skill extraction
│   ├── question_engine.py       # Dataset loading + question selection
│   ├── answer_evaluator.py      # Core ML/NLP answer scoring
│   └── recommendation.py        # Weak-topic detection + recommendations
├── utils/
│   └── text_processing.py       # Tokenization, stop-word removal, lemmatization
└── assets/                      # (reserved for images/icons)
```

## 11. Dataset Description
`data/interview_questions.csv` contains **100 original, hand-authored questions**
across 10 categories (10 questions each): Python, Machine Learning, Artificial
Intelligence, DBMS, SQL, Data Structures, Algorithms, Computer Networks, OOP, and
Basic Statistics. Each row has the following fields:

| Column | Description |
|---|---|
| `question_id` | Unique ID, e.g. `Q001` |
| `category` | One of the 10 subject categories |
| `topic` | Specific sub-topic within the category |
| `difficulty` | Easy / Medium / Hard |
| `question` | The interview question text |
| `expected_answer` | A model/reference answer used for similarity comparison |
| `keywords` | Comma-separated key concepts expected in a good answer |

This is an **original educational dataset** created for this project; it is not
scraped or copied from any external source.

## 12. ML/NLP Methodology
1. **Text preprocessing** (`utils/text_processing.py`): lowercasing, punctuation
   removal, tokenization, stop-word removal, and lemmatization.
2. **TF-IDF vectorization**: the student's answer and the expected answer are each
   converted into a TF-IDF vector using `sklearn.feature_extraction.text.TfidfVectorizer`.
3. **Cosine similarity**: the angle between the two TF-IDF vectors is computed with
   `sklearn.metrics.pairwise.cosine_similarity`, producing a semantic similarity
   score between 0–100%.
4. **Keyword matching (rule-based)**: a simple set-based comparison checks how many
   of the dataset's expected keywords appear in the student's (preprocessed) answer.
5. **Final score**: a weighted blend — 70% TF-IDF/cosine similarity + 30% keyword
   match — is used as the final score, so the evaluation is not a plain string match.
6. **Weak-topic identification**: rule-based aggregation (average score per topic,
   compared against a threshold) run over the SQLite history.

**Honesty note:** Skill extraction from resumes and weak-topic aggregation are
explicitly rule-based (dictionary lookup / averaging), not trained ML models. The
genuine machine-learning/NLP component of this project is the TF-IDF + cosine
similarity answer evaluator described above.

## 13. System Workflow
1. Student creates a profile.
2. Student uploads resume → text extracted → skills extracted → stored in DB.
3. Student selects a category and difficulty → questions sampled from dataset.
4. Student answers each question → TF-IDF/cosine similarity + keyword score computed
   → final score & feedback shown → saved to DB.
5. Dashboard aggregates all past sessions → charts + weak-topic recommendations.

## 14. Limitations
- TF-IDF captures lexical/semantic overlap but not true deep contextual
  understanding (unlike transformer-based embeddings).
- Skill extraction is limited to a fixed, curated vocabulary.
- Question bank is static (100 questions); no dynamic question generation via a
  language model.
- Designed for single-user/local demonstration use (SQLite, not a multi-user
  production database).

## 15. Future Scope
- Replace TF-IDF with sentence embeddings (e.g. Sentence-BERT) for deeper semantic
  scoring.
- Add a fine-tuned/LLM-based question generator instead of a static CSV bank.
- Add voice-based answer input with speech-to-text.
- Deploy with a multi-user database (PostgreSQL) and authentication.
- Add resume-quality scoring and formatting suggestions.

## 16. Conclusion
This project demonstrates a complete, working application of NLP and Machine Learning
techniques — text preprocessing, TF-IDF vectorization, and cosine similarity — to solve
a genuine, practical problem for engineering students: objective, automated feedback on
interview answer quality, combined with performance tracking to guide focused revision.

---

## 17. Deployment

### Option A — Streamlit Community Cloud (recommended, free, runs the real app)

1. Push the project to GitHub:
   ```bash
   git add -A
   git commit -m "Update project"
   git push origin main
   ```
2. Go to https://share.streamlit.io/ and sign in with your GitHub account.
3. Click **Create app → Deploy an existing app**.
4. Fill in:
   | Field | Value |
   |---|---|
   | Repository | `l9729285407-ship-it/AI-Interview-Assistant` |
   | Branch | `main` |
   | Main file path | `app.py` |
5. Click **Deploy**. Your app will be live at `https://<app-name>.streamlit.app`.

**Cloud notes:**
- The SQLite database (`data/interview_assistant.db`) lives on the ephemeral
  container, so history resets on redeploy/restart. For permanent storage, move to
  PostgreSQL (see Future Scope).
- The first run downloads the NLTK datasets (punkt, stopwords, wordnet).

### Option B — Vercel (project landing page)

Vercel's serverless Python runtime only supports WSGI/ASGI frameworks such as Flask and
FastAPI. Streamlit needs a long-running WebSocket server plus persistent disk, so it
**cannot run inside Vercel functions** (an earlier config pointing `@vercel/python` at
`app.py` would fail the build, since `app.py` exports no WSGI application).

`vercel.json` is therefore set up as a **static build** that serves `public/index.html`
— a landing page linking to the live Streamlit app and this repository:

1. Go to https://vercel.com → **Add New… → Project**.
2. Import `l9729285407-ship-it/AI-Interview-Assistant` from GitHub.
3. Keep the default settings (no framework preset is required) → **Deploy**.
4. Your landing page goes live at `https://<project>.vercel.app`.

> Tip: edit `public/index.html` and replace the "Open the Live App" URL with your actual
> Streamlit Cloud address after Option A finishes deploying.
