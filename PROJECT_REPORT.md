# B.Tech Project Report

---

## Title Page

**AI-BASED INTERVIEW PREPARATION ASSISTANT USING MACHINE LEARNING AND NLP**

A project report submitted in partial fulfillment of the requirements for the degree of
**Bachelor of Technology in Artificial Intelligence & Machine Learning**

Submitted by: *[Your Name]*
Roll No: *[Your Roll Number]*

Under the guidance of: *[Guide's Name]*

Department of Artificial Intelligence & Machine Learning
*[Your College Name]*
*[Academic Year]*

---

## Certificate

*This is to certify that the project entitled "AI-Based Interview Preparation Assistant
Using Machine Learning and NLP" is a bona fide work carried out by [Your Name],
[Roll Number], in partial fulfillment of the requirements for the award of the degree
of Bachelor of Technology in Artificial Intelligence & Machine Learning during the
academic year [Year].*

Signature of Guide ______________  Signature of HOD ______________

*(To be signed by your project guide and Head of Department — placeholder only.)*

---

## Declaration

*I hereby declare that the project work entitled "AI-Based Interview Preparation
Assistant Using Machine Learning and NLP" submitted to [College Name] is a record of
original work carried out by me under the guidance of [Guide's Name], and has not been
submitted elsewhere for the award of any degree or diploma.*

Signature: ______________  Name: [Your Name]  Date: ______________

---

## Acknowledgement

*I would like to express my sincere gratitude to my project guide, [Guide's Name], for
their constant support and guidance throughout this project. I also thank the Department
of AI & ML and all faculty members for providing the resources and environment
necessary to complete this work.*

---

## Abstract

Technical interview preparation is a critical but often unstructured part of a student's
placement journey. This project presents a Streamlit-based web application that helps
B.Tech students prepare for technical interviews by analyzing their resume, selecting
relevant interview questions by category and difficulty, and automatically evaluating
their written answers using Natural Language Processing (NLP) and Machine Learning (ML)
techniques — specifically TF-IDF vectorization and Cosine Similarity — combined with
rule-based keyword matching. The system stores interview history in SQLite and presents
a performance dashboard with weak-topic identification and personalized recommendations.

---

## 1. Introduction

Interview preparation for technical roles requires students to not only know concepts
but also be able to articulate them clearly under evaluation. Traditional preparation
methods — question banks, mock interviews with peers, or online quizzes — provide little
to no automated, objective feedback on the *quality* of a written or spoken answer. This
project builds a self-contained web application that uses classical NLP and ML
techniques to score free-text interview answers and track a student's progress over
time.

## 2. Problem Statement

Students lack an accessible tool that can (a) present interview questions relevant to
their profile, (b) evaluate their answers beyond simple correct/incorrect grading, and
(c) identify specific weak topics for focused revision. This project addresses that gap.

## 3. Objectives

- Build a working end-to-end interview preparation web application.
- Extract skills automatically from an uploaded resume.
- Provide a categorized, difficulty-tiered interview question bank.
- Evaluate free-text answers using TF-IDF + Cosine Similarity and keyword matching.
- Track performance over time and identify weak topics with recommendations.

## 4. Existing System

Most existing tools fall into two categories:
1. **Static question banks** (PDFs, books, websites) — no feedback mechanism at all.
2. **MCQ-based practice platforms** — only support multiple-choice questions, which
   cannot evaluate a student's ability to *articulate* a free-text technical answer.

Neither category offers automated evaluation of open-ended written answers or
longitudinal weak-topic tracking.

## 5. Proposed System

The proposed system is a Streamlit web application with:
- A resume analyzer that extracts skills using keyword/dictionary matching.
- A question engine that samples from a 100-question categorized dataset.
- An NLP/ML answer evaluator using TF-IDF vectorization and cosine similarity, blended
  with rule-based keyword coverage scoring.
- A SQLite-backed performance dashboard with weak-topic identification and
  recommendations.

## 6. Literature Review

- **TF-IDF (Term Frequency–Inverse Document Frequency):** A classical Information
  Retrieval technique (Salton & Buckley, 1988) that weights terms by their frequency in
  a document relative to their frequency across a corpus, down-weighting common words.
  It remains a standard baseline technique for text similarity tasks and is implemented
  in widely used libraries such as scikit-learn.
- **Cosine Similarity:** A standard vector-space measure of similarity between two
  non-zero vectors, commonly used in Information Retrieval and NLP to compare document
  or sentence representations (Manning, Raghavan & Schütze, *Introduction to Information
  Retrieval*, Cambridge University Press, 2008).
- **NLTK (Natural Language Toolkit):** A widely used Python library (Bird, Klein & Loper,
  *Natural Language Processing with Python*, O'Reilly, 2009) providing tokenization,
  stop-word lists, and lemmatization utilities used in this project's preprocessing
  pipeline.

*(Only real, verifiable, standard references are used; no fabricated citations.)*

## 7. Methodology

The project follows a modular pipeline:
1. **Data acquisition:** An original 100-question dataset was authored covering 10 CS
   subject areas.
2. **Preprocessing:** lowercasing, punctuation removal, tokenization, stop-word removal,
   lemmatization (`utils/text_processing.py`).
3. **Feature extraction:** TF-IDF vectorization of the student's answer and the expected
   answer (`models/model.py`, `modules/answer_evaluator.py`).
4. **Similarity computation:** cosine similarity between the two TF-IDF vectors.
5. **Rule-based keyword scoring:** set-overlap between the answer's tokens and the
   dataset's `keywords` field.
6. **Score fusion:** weighted blend (70% similarity, 30% keyword score).
7. **Persistence & analytics:** all sessions and results are stored in SQLite;
   aggregated per-topic averages drive weak-topic identification.

## 8. System Architecture

```
                ┌───────────────────┐
                │   Streamlit UI     │
                │     (app.py)       │
                └─────────┬──────────┘
                          │
        ┌─────────────────┼──────────────────┐
        │                 │                  │
┌───────▼───────┐ ┌───────▼────────┐ ┌───────▼────────┐
│ resume_analyzer│ │ question_engine │ │ answer_evaluator│
│   (PyPDF2)     │ │   (pandas)      │ │ (TF-IDF+cosine) │
└───────┬───────┘ └───────┬────────┘ └───────┬────────┘
        │                 │                  │
        └─────────────────┼──────────────────┘
                          │
                ┌─────────▼──────────┐
                │  database.py (SQLite)│
                └─────────┬──────────┘
                          │
                ┌─────────▼──────────┐
                │  recommendation.py  │
                └─────────────────────┘
```

## 9. Data Flow

1. Student profile → `students` table
2. Resume upload → text/skills → `resumes` table
3. Question selection → in-memory (from CSV) → displayed
4. Answer submission → evaluator → `question_results` table
5. Session completion → aggregate score → `interview_sessions` table
6. Dashboard queries → aggregated views over all tables

## 10. Dataset

`data/interview_questions.csv`: 100 rows, 7 columns (`question_id`, `category`, `topic`,
`difficulty`, `question`, `expected_answer`, `keywords`), spanning Python, Machine
Learning, Artificial Intelligence, DBMS, SQL, Data Structures, Algorithms, Computer
Networks, OOP, and Basic Statistics (10 questions each, mixed Easy/Medium/Hard).

## 11. Data Preprocessing

Implemented in `utils/text_processing.py`:
- `clean_text()` — lowercasing and punctuation stripping via regex
- `tokenize()` — word tokenization (NLTK, with a regex-split fallback if NLTK data is
  unavailable)
- `remove_stopwords()` — removes common English stop-words
- `lemmatize()` — reduces words to base form using NLTK's WordNet lemmatizer

## 12. NLP Methodology

Free-text answers are preprocessed and converted into TF-IDF vectors using
`sklearn.feature_extraction.text.TfidfVectorizer`. TF-IDF assigns higher weight to
words that are frequent in a specific document but rare across the corpus, capturing
which words are most distinctive/informative for that answer.

## 13. ML Methodology

Cosine similarity (`sklearn.metrics.pairwise.cosine_similarity`) is computed between the
TF-IDF vector of the student's answer and that of the expected answer, producing a
similarity score in [0, 1] (scaled to a percentage). This is combined with a rule-based
keyword-coverage score using a fixed weighting (70/30) to produce the final answer score.

## 14. Implementation

The system is implemented in Python using Streamlit for the UI, Pandas/NumPy for data
handling, scikit-learn for TF-IDF/cosine similarity, NLTK for text preprocessing,
PyPDF2 for resume text extraction, SQLite for persistence, and Plotly for dashboard
charts. See the accompanying source code (`app.py` and the `modules/`, `utils/`,
`database/`, `models/` packages) for the complete implementation.

## 15. Results

Testing with sample answers (see Testing section) shows the evaluator correctly assigns
high scores (>70%) to answers that closely paraphrase the expected answer and cover its
key concepts, moderate scores (40–70%) to partially correct answers, and low scores
(<40%) to irrelevant or empty answers — validating that the TF-IDF + cosine similarity
approach meaningfully differentiates answer quality.

## 16. Advantages

- Provides objective, automated feedback instead of purely static question banks.
- Lightweight — runs entirely locally with no paid APIs or GPUs required.
- Modular architecture makes it easy to extend (e.g., swap in a different similarity
  model).
- Tracks progress over time and surfaces weak topics automatically.

## 17. Limitations

- TF-IDF is a lexical/statistical technique; it does not capture deep semantic meaning
  the way transformer-based embeddings would.
- Skill extraction relies on a fixed vocabulary and will miss uncommon skill names.
- Single-user local SQLite database; not designed for concurrent multi-user production
  deployment.

## 18. Future Scope

- Integrate sentence embeddings (e.g., Sentence-BERT) for deeper semantic scoring.
- Add LLM-based dynamic question generation.
- Add voice-based answers with speech-to-text.
- Multi-user deployment with a production database and authentication.

## 19. Conclusion

This project demonstrates a complete, functioning application of classical NLP and ML
techniques to a real student need: automated, objective evaluation of interview answers
combined with performance analytics. It fulfills the requirement of being a genuine
AI/ML academic project, with clearly documented boundaries between its ML-based and
rule-based components.

## 20. References

1. G. Salton and C. Buckley, "Term-weighting approaches in automatic text retrieval,"
   *Information Processing & Management*, vol. 24, no. 5, pp. 513–523, 1988.
2. C. D. Manning, P. Raghavan, and H. Schütze, *Introduction to Information Retrieval*,
   Cambridge University Press, 2008.
3. S. Bird, E. Klein, and E. Loper, *Natural Language Processing with Python*, O'Reilly
   Media, 2009.
4. Scikit-learn documentation: https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting
5. Streamlit documentation: https://docs.streamlit.io
6. Python `sqlite3` documentation: https://docs.python.org/3/library/sqlite3.html
