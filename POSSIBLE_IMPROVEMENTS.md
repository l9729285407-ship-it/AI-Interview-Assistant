# Possible Improvements

1. **Deeper semantic scoring** — Replace/augment TF-IDF with Sentence-BERT or other
   transformer-based sentence embeddings for more accurate semantic similarity,
   especially for answers that are correct but phrased very differently from the
   expected answer.
2. **ML-based skill extraction** — Train a Named Entity Recognition (NER) model on
   labeled resumes instead of dictionary lookup, to catch skills outside the fixed
   vocabulary.
3. **Dynamic question generation** — Use a language model to generate fresh questions
   on demand instead of relying solely on the static 100-question CSV.
4. **Voice-based interviews** — Add speech-to-text so students can practice speaking
   answers aloud, closer to a real interview experience.
5. **Adaptive difficulty** — Automatically increase/decrease difficulty based on the
   student's running performance within a session.
6. **Multi-user deployment** — Move from SQLite to PostgreSQL/MySQL with proper user
   authentication for classroom or institution-wide deployment.
7. **Resume quality scoring** — Give feedback on resume formatting, length, and
   completeness, not just skill extraction.
8. **Explainable feedback** — Highlight which specific sentences/keywords in the
   student's answer contributed most to the similarity score.
9. **Peer/mentor review integration** — Allow a mentor to add manual comments on top of
   the automated score.
10. **Mobile-friendly UI** — Further optimize the Streamlit layout for smaller screens,
    or build a dedicated mobile front-end.
