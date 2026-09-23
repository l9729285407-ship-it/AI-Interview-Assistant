"""
models/model.py

Thin wrapper class around the scikit-learn TF-IDF + Cosine Similarity model
used for answer evaluation. Kept separate from modules/answer_evaluator.py
so the "ML model" has a clear, dedicated home in the project architecture,
matching standard ML project layouts (models/ folder).

This does NOT persist a trained model to disk because TF-IDF here is fit
fresh on each (expected_answer, user_answer) pair -- this is a standard,
lightweight approach for short-text semantic similarity and avoids the
complexity of managing a large pre-trained vocabulary for a college project.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TfidfSimilarityModel:
    """
    A minimal, self-contained ML model class exposing a scikit-learn
    TfidfVectorizer + cosine similarity pipeline.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def fit_transform_pair(self, text_a: str, text_b: str):
        """Fit the TF-IDF vectorizer on two documents and return their vectors."""
        if not text_a.strip() or not text_b.strip():
            raise ValueError("Both input texts must be non-empty for TF-IDF vectorization.")
        matrix = self.vectorizer.fit_transform([text_a, text_b])
        return matrix

    def similarity(self, text_a: str, text_b: str) -> float:
        """Return cosine similarity between two texts, as a float in [0, 1]."""
        matrix = self.fit_transform_pair(text_a, text_b)
        sim = cosine_similarity(matrix[0:1], matrix[1:2])
        return float(sim[0][0])

    def get_feature_names(self):
        """Return the vocabulary learned during the last fit_transform call."""
        try:
            return self.vectorizer.get_feature_names_out().tolist()
        except Exception:
            return []
