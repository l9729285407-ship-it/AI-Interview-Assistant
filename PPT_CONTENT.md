# PPT Content — 15 Slides
### AI-Based Interview Preparation Assistant Using Machine Learning and NLP

---

**Slide 1 — Title**
- AI-Based Interview Preparation Assistant Using Machine Learning and NLP
- B.Tech AI & ML Final Year Project
- [Your Name] | [Roll No] | [Guide Name] | [College Name]

**Slide 2 — Introduction**
- Interview prep tools today are mostly static question banks
- No feedback on the *quality* of a written answer
- This project brings NLP/ML-based evaluation to interview prep

**Slide 3 — Problem Statement**
- Students can't objectively evaluate their own interview answers
- No tracking of weak topics over time
- Preparation is unstructured and generic, not personalized

**Slide 4 — Objectives**
- Build an end-to-end interview prep web app
- Extract skills from resumes automatically
- Evaluate free-text answers using TF-IDF + Cosine Similarity
- Track performance & recommend weak topics

**Slide 5 — Existing System**
- Static PDFs / question banks — no feedback
- MCQ practice platforms — can't evaluate open-ended answers
- No personalized, longitudinal weak-topic tracking

**Slide 6 — Proposed System**
- Resume analyzer (skill extraction)
- Category + difficulty based question selection
- NLP/ML answer evaluation (TF-IDF + cosine similarity)
- Performance dashboard + recommendations

**Slide 7 — System Architecture**
- Streamlit UI → Resume Analyzer / Question Engine / Answer Evaluator
- All backed by SQLite database
- Recommendation engine reads from stored history
- (Insert architecture diagram from report Section 8)

**Slide 8 — Technologies Used**
- Python, Streamlit
- Pandas, NumPy
- Scikit-learn (TF-IDF, Cosine Similarity)
- NLTK (tokenization, stop-words, lemmatization)
- PyPDF2, SQLite, Plotly

**Slide 9 — Dataset**
- 100 original questions across 10 categories
- Fields: question_id, category, topic, difficulty, question, expected_answer, keywords
- Categories: Python, ML, AI, DBMS, SQL, Data Structures, Algorithms, Networks, OOP, Statistics

**Slide 10 — NLP/ML Methodology**
- Preprocessing: tokenization, stop-word removal, lemmatization
- TF-IDF vectorization of student vs. expected answer
- Cosine similarity → semantic similarity score
- Rule-based keyword matching → coverage score
- Weighted blend (70/30) → final score

**Slide 11 — Implementation**
- Modular codebase: modules/, utils/, database/, models/
- Streamlit multi-page app with sidebar navigation
- SQLite persistence for students, resumes, sessions, results

**Slide 12 — Screenshots / Placeholders**
- [Insert screenshot: Dashboard]
- [Insert screenshot: Mock Interview page]
- [Insert screenshot: Result page with scores]
- [Insert screenshot: Performance dashboard charts]

**Slide 13 — Results**
- High-similarity answers scored consistently higher than irrelevant answers
- Keyword scoring correctly identifies concept coverage
- Weak-topic detection validated against sample session data

**Slide 14 — Future Scope**
- Sentence-BERT embeddings for deeper semantic scoring
- LLM-based dynamic question generation
- Voice-based answers with speech-to-text
- Multi-user deployment with production database

**Slide 15 — Conclusion**
- Delivered a working, complete AI/ML academic project
- Demonstrates real NLP/ML techniques (TF-IDF, cosine similarity)
- Provides genuine value: objective feedback + progress tracking
- Thank You / Questions
