"""
modules/answer_evaluator.py

This is the CORE MACHINE LEARNING / NLP MODULE of the project.

Technique used: TF-IDF (Term Frequency - Inverse Document Frequency) vectorization
combined with Cosine Similarity, implemented via scikit-learn.

Why this is genuine ML/NLP (not just string matching):
    - TF-IDF is a statistical feature-extraction technique from Information Retrieval
      and NLP that learns how important each word is across a "corpus" (here, the
      student's answer and the expected answer), down-weighting common words.
    - Cosine similarity measures the angle between the two TF-IDF vectors in a
      high-dimensional vector space, a standard technique used in real-world
      semantic-similarity and search-ranking systems.

In addition to the ML-based similarity score, a separate RULE-BASED keyword-overlap
score is computed (simple set intersection against the dataset's `keywords` field).
The two scores are blended into a final score. This blend, and which parts are rule
based vs. ML based, is explicitly disclosed to keep the project academically honest.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.text_processing import preprocess_to_string, preprocess


class AnswerEvaluationError(Exception):
    pass


def compute_tfidf_cosine_similarity(user_answer: str, expected_answer: str) -> float:
    """
    ML/NLP COMPONENT:
    Vectorizes the user's answer and the expected answer using TF-IDF, then computes
    cosine similarity between the two vectors. Returns a similarity score in [0, 100].
    """
    user_clean = preprocess_to_string(user_answer)
    expected_clean = preprocess_to_string(expected_answer)

    if not user_clean or not expected_clean:
        return 0.0

    try:
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([expected_clean, user_clean])
        similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        similarity_score = float(similarity_matrix[0][0])
        return round(similarity_score * 100, 2)
    except ValueError:
        # Happens if, after preprocessing, the vocabulary is empty (e.g. answer was
        # only stop-words or symbols)
        return 0.0


def compute_keyword_match_score(user_answer: str, keywords: str) -> float:
    """
    RULE-BASED COMPONENT (explicitly not ML):
    Computes the fraction of expected keywords that appear (after lemmatization)
    in the student's answer. Returns a score in [0, 100].
    """
    if not keywords:
        return 0.0

    keyword_list = [k.strip().lower() for k in keywords.split(",") if k.strip()]
    if not keyword_list:
        return 0.0

    user_tokens = set(preprocess(user_answer))

    matched = 0
    for kw in keyword_list:
        kw_tokens = set(preprocess(kw))
        if kw_tokens and kw_tokens.issubset(user_tokens):
            matched += 1
        elif kw_tokens & user_tokens:  # partial match for multi-word keywords
            matched += 0.5

    score = (matched / len(keyword_list)) * 100
    return round(min(score, 100.0), 2)


def generate_feedback(similarity_score: float, keyword_score: float, final_score: float) -> str:
    """Generate human-readable, rule-based feedback text from the computed scores."""
    if final_score >= 80:
        verdict = "Excellent answer! You demonstrated a strong understanding of the concept."
    elif final_score >= 60:
        verdict = "Good answer, but there is room to include more detail or precision."
    elif final_score >= 40:
        verdict = "Average answer. You covered some relevant points but missed key concepts."
    else:
        verdict = "This answer needs significant improvement. Review this topic before your interview."

    details = (
        f"Semantic similarity to the model answer (TF-IDF + cosine similarity): {similarity_score}%. "
        f"Keyword coverage (rule-based matching): {keyword_score}%."
    )

    return f"{verdict} {details}"


def evaluate_answer(user_answer: str, expected_answer: str, keywords: str,
                     similarity_weight: float = 0.7, keyword_weight: float = 0.3):
    """
    Full evaluation pipeline for a single question-answer pair.

    Final score = (similarity_weight * TF-IDF cosine similarity) + (keyword_weight * keyword match)

    Returns a dict with all intermediate and final scores plus feedback.
    """
    if user_answer is None or not user_answer.strip():
        raise AnswerEvaluationError("Answer cannot be empty. Please provide a response before submitting.")

    similarity_score = compute_tfidf_cosine_similarity(user_answer, expected_answer)
    keyword_score = compute_keyword_match_score(user_answer, keywords)

    final_score = round((similarity_weight * similarity_score) + (keyword_weight * keyword_score), 2)
    final_score = max(0.0, min(100.0, final_score))

    feedback = generate_feedback(similarity_score, keyword_score, final_score)

    return {
        "similarity_score": similarity_score,
        "keyword_score": keyword_score,
        "final_score": final_score,
        "feedback": feedback,
    }
