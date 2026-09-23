"""
modules/recommendation.py

Generates weak-topic identification and study recommendations based on a
student's historical performance stored in SQLite.

Technique: rule-based aggregation (average score per topic) + simple
threshold-based recommendation logic. This is explicitly disclosed as
rule-based, not a trained ML recommender model.
"""

from database import database as db

STUDY_RESOURCES = {
    "Python": "Revise functions, OOP, and exception handling. Practice on HackerRank's Python track.",
    "Machine Learning": "Revisit supervised vs unsupervised learning, overfitting, and evaluation metrics.",
    "Artificial Intelligence": "Review search algorithms, heuristics, and knowledge representation basics.",
    "DBMS": "Focus on normalization, ACID properties, and indexing concepts.",
    "SQL": "Practice writing JOIN, GROUP BY, and subquery queries on sample databases.",
    "Data Structures": "Revise arrays, linked lists, trees, and hashing with implementation practice.",
    "Algorithms": "Focus on sorting, searching, recursion, and Big-O complexity analysis.",
    "Computer Networks": "Review the OSI model, TCP/UDP differences, and basic network security.",
    "OOP": "Revise the four pillars: encapsulation, abstraction, inheritance, polymorphism.",
    "Basic Statistics": "Review mean/median/mode, standard deviation, and probability basics.",
}


def identify_weak_topics(student_id, threshold=50.0):
    """Return a list of dicts describing topics where the student scores below threshold."""
    return db.get_weak_topics(student_id, threshold=threshold)


def generate_recommendations(student_id, threshold=50.0):
    """
    Combine weak-topic identification with a static study-resource lookup
    to produce actionable recommendations.
    """
    weak_topics = identify_weak_topics(student_id, threshold=threshold)

    if not weak_topics:
        return [{
            "topic": "General",
            "message": "Great job! No significantly weak topics detected yet. Keep practicing "
                       "across all categories to maintain your performance."
        }]

    recommendations = []
    for item in weak_topics:
        topic = item["topic"]
        avg_score = round(item["avg_score"], 2)
        resource = STUDY_RESOURCES.get(topic, "Revisit the fundamentals of this topic and practice more questions.")
        recommendations.append({
            "topic": topic,
            "average_score": avg_score,
            "attempts": item["attempts"],
            "message": f"Your average score in '{topic}' is {avg_score}%. Suggestion: {resource}",
        })

    return recommendations
