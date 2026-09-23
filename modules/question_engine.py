"""
modules/question_engine.py

Handles loading the interview question dataset and selecting questions
based on category, difficulty, and (optionally) skills extracted from
the student's resume.
"""

import os
import random
import pandas as pd

DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "interview_questions.csv"
)

REQUIRED_COLUMNS = ["question_id", "category", "topic", "difficulty", "question", "expected_answer", "keywords"]


class QuestionEngineError(Exception):
    """Raised when the question dataset is missing or malformed."""
    pass


def load_questions() -> pd.DataFrame:
    """Load and validate the question dataset CSV."""
    if not os.path.exists(DATA_PATH):
        raise QuestionEngineError(
            "The interview question dataset (data/interview_questions.csv) was not found. "
            "Please make sure the file exists in the data/ folder."
        )

    try:
        df = pd.read_csv(DATA_PATH)
    except Exception as e:
        raise QuestionEngineError(f"Failed to read the question dataset: {e}")

    missing_cols = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing_cols:
        raise QuestionEngineError(
            f"The dataset is missing required columns: {', '.join(missing_cols)}"
        )

    if df.empty:
        raise QuestionEngineError("The question dataset is empty.")

    return df


def get_categories():
    """Return a sorted list of unique interview categories."""
    df = load_questions()
    return sorted(df["category"].dropna().unique().tolist())


def get_difficulties():
    return ["Easy", "Medium", "Hard"]


def select_questions(category: str, difficulty: str, num_questions: int = 5, seed: int = None):
    """
    Select `num_questions` questions matching the given category and difficulty.
    Falls back gracefully (with a message) if not enough matching questions exist.
    Returns a list of dicts.
    """
    df = load_questions()

    filtered = df[(df["category"] == category) & (df["difficulty"] == difficulty)]

    if filtered.empty:
        # Fall back to category only if difficulty has no matches
        filtered = df[df["category"] == category]

    if filtered.empty:
        raise QuestionEngineError(
            f"No questions found for category '{category}'. Please choose a different category."
        )

    n = min(num_questions, len(filtered))
    if seed is not None:
        sampled = filtered.sample(n=n, random_state=seed)
    else:
        sampled = filtered.sample(n=n)

    return sampled.to_dict(orient="records")


def recommend_questions_by_skills(skills, num_questions: int = 5):
    """
    Recommend questions whose category/topic loosely matches skills extracted
    from the student's resume (simple rule-based matching, not ML).
    """
    df = load_questions()
    if not skills:
        return select_questions(random.choice(df["category"].unique().tolist()), "Easy", num_questions)

    skill_text = " ".join(skills).lower()
    mask = df.apply(
        lambda row: row["category"].lower() in skill_text or row["topic"].lower() in skill_text,
        axis=1,
    )
    matched = df[mask]

    if matched.empty:
        matched = df

    n = min(num_questions, len(matched))
    return matched.sample(n=n).to_dict(orient="records")
