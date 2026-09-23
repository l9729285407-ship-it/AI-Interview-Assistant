# Viva Preparation

## Part A — 30+ Viva Questions with Answers

### AI / ML / NLP Concepts
1. **What is Artificial Intelligence?**
   The simulation of human intelligence in machines that can learn, reason, and make decisions.

2. **What is Machine Learning?**
   A subset of AI where systems learn patterns from data rather than being explicitly programmed.

3. **What is NLP?**
   Natural Language Processing — the field of AI concerned with enabling computers to understand and process human language.

4. **What is TF-IDF?**
   A statistical measure (Term Frequency × Inverse Document Frequency) that scores how important a word is to a document relative to a collection of documents, down-weighting common words.

5. **Why use TF-IDF instead of simple word counting?**
   Simple word counts overweight common words like "the" or "is". TF-IDF reduces their weight and boosts distinctive, informative terms.

6. **What is Cosine Similarity?**
   A measure of similarity between two non-zero vectors based on the cosine of the angle between them; a value of 1 means identical direction (very similar), 0 means orthogonal (unrelated).

7. **Why cosine similarity and not Euclidean distance for text?**
   Cosine similarity is unaffected by document length/magnitude, which matters for text where answer length varies; it captures directional (word-usage pattern) similarity.

8. **Is your project using a "deep learning" model?**
   No — it deliberately uses classical, lightweight NLP/ML techniques (TF-IDF + cosine similarity) suitable for a college project without GPU requirements.

9. **What is tokenization?**
   Splitting text into smaller units (usually words) for further processing.

10. **What are stop-words and why remove them?**
    Common words (e.g., "the", "is", "and") that carry little semantic meaning; removing them helps the model focus on meaningful content words.

11. **What is lemmatization? How is it different from stemming?**
    Lemmatization reduces a word to its dictionary base form (e.g., "running" → "run") using vocabulary and grammar rules, producing valid words, unlike stemming which crudely chops suffixes and can produce non-words.

12. **Is skill extraction from resumes an ML model?**
    No — it is explicitly rule-based, using dictionary/keyword matching against a curated skills vocabulary, not a trained classifier.

13. **How would you make skill extraction ML-based instead?**
    By training a Named Entity Recognition (NER) model on labeled resume data to identify skill entities automatically.

### Project-Specific
14. **What problem does your project solve?**
    It gives students automated, objective feedback on free-text interview answers and tracks their weak topics over time — something static question banks can't do.

15. **How is a student's answer evaluated?**
    Preprocessed, converted to a TF-IDF vector, compared via cosine similarity to the expected answer's vector, and blended with a rule-based keyword-coverage score (70/30 weighting).

16. **What database do you use and why?**
    SQLite — a lightweight, file-based, serverless database that requires no separate installation, ideal for a single-user local demo.

17. **What tables does your database have?**
    `students`, `resumes`, `interview_sessions`, and `question_results`.

18. **How do you identify weak topics?**
    By averaging a student's scores per topic across all their sessions and flagging topics below a set threshold (default 50%).

19. **Why Streamlit for the UI?**
    Streamlit lets you build a data-driven, interactive web UI purely in Python, ideal for rapid development of an ML-powered application without separate frontend code.

20. **How do you extract text from a resume PDF?**
    Using the PyPDF2 library, which reads each page of the PDF and extracts its text content.

21. **What happens if a PDF has no extractable text?**
    The app catches this with a `ResumeAnalysisError` and shows a friendly message that the file may be a scanned image and asks for a text-based PDF.

22. **What is your dataset and how big is it?**
    An original 100-question dataset spanning 10 categories (Python, ML, AI, DBMS, SQL, Data Structures, Algorithms, Computer Networks, OOP, Basic Statistics).

23. **How are questions selected for a mock interview?**
    Randomly sampled from the dataset filtered by the chosen category and difficulty using pandas' `.sample()`.

24. **What is the final score formula?**
    `final_score = 0.7 × similarity_score + 0.3 × keyword_score`, clipped to [0, 100].

25. **Why weight similarity higher than keyword matching?**
    Because semantic similarity better captures whether the *meaning* of the answer is correct, while keyword matching alone can be gamed by just listing terms.

### Architecture / Engineering
26. **Why did you separate the code into modules/, utils/, database/, models/?**
    For separation of concerns and maintainability — each folder has a single responsibility, matching standard software engineering practice.

27. **How does your app handle errors (e.g., missing dataset, empty answer)?**
    Custom exceptions (`QuestionEngineError`, `ResumeAnalysisError`, `AnswerEvaluationError`) are raised by the relevant module and caught in `app.py`, which shows a user-friendly Streamlit error message instead of crashing.

28. **What happens if NLTK data can't be downloaded (no internet)?**
    The text-processing module falls back to a static stop-word list and regex-based tokenization/skips lemmatization, so the app still works end-to-end offline.

29. **How would you scale this to multiple concurrent users?**
    Replace SQLite with a production database like PostgreSQL, add user authentication, and deploy behind a WSGI/ASGI server instead of local Streamlit.

### Limitations / Future Scope
30. **What are the limitations of your project?**
    TF-IDF doesn't capture deep semantic meaning like transformer embeddings would; skill extraction is limited to a fixed vocabulary; it's built for single-user local demonstration.

31. **What would you improve given more time?**
    Use Sentence-BERT embeddings for more accurate semantic scoring, add LLM-based dynamic question generation, and support voice-based answers via speech-to-text.

32. **Why did you choose this project topic?**
    It combines genuine NLP/ML techniques with a practical, relatable problem for engineering students, making it both academically rigorous and personally useful.

---

## Part B — 2-Minute Spoken Explanation

"Good [morning/afternoon]. My project is an AI-Based Interview Preparation Assistant
built using Machine Learning and NLP. The problem I'm solving is that most interview
preparation tools — question banks, PDFs, MCQ apps — give students no real feedback on
how good their *written* answers actually are.

My application is a Streamlit web app where a student first uploads their resume, which
I parse using PyPDF2, and from which I extract their technical skills using keyword
matching. The student then picks an interview category — like Python, DBMS, or Machine
Learning — and a difficulty level, and the app pulls questions from a dataset of 100
original questions I created myself.

The core of the project is how I evaluate the student's answer. I preprocess both the
student's answer and a reference expected answer — lowercasing, tokenizing, removing
stop-words, and lemmatizing — and then convert both into TF-IDF vectors using
scikit-learn. I compute the cosine similarity between those two vectors, which gives me
a semantic similarity score. I combine that with a simpler rule-based keyword-coverage
check, weighted 70-30, to get a final score, and I generate feedback text based on that
score.

Every answer, score, and session gets stored in a SQLite database, so I can show the
student a performance dashboard with charts of their progress over time, and I can
identify which topics they're consistently weak in and recommend what to study next.

I was careful throughout the project to be honest about which parts are genuine machine
learning — the TF-IDF and cosine similarity answer evaluation — versus which parts are
simpler rule-based logic, like resume skill extraction and weak-topic averaging. Overall,
this project shows a complete, working pipeline: text preprocessing, feature extraction,
similarity-based scoring, and data-driven feedback, applied to a problem that's genuinely
useful for students like me. Thank you."
