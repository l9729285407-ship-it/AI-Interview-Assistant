"""
modules/resume_analyzer.py

Responsible for:
    1. Extracting raw text from an uploaded resume PDF (PyPDF2)
    2. Extracting technical skills from that text using rule-based keyword matching
       against a curated skills dictionary.

NOTE ON AI/ML HONESTY:
Skill extraction here is a RULE-BASED / dictionary-lookup technique (string matching
against a known skills vocabulary), not a trained ML classifier. This is called out
explicitly in the README and report. The genuine ML/NLP component of this project is
the TF-IDF + cosine similarity answer evaluator in answer_evaluator.py.
"""

import PyPDF2

from utils.text_processing import clean_text

# A curated vocabulary of common technical skills relevant to CS/AI-ML students.
SKILLS_DB = [
    "python", "java", "c++", "c", "javascript", "sql", "html", "css",
    "machine learning", "deep learning", "artificial intelligence", "nlp",
    "natural language processing", "computer vision", "data science",
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch",
    "django", "flask", "streamlit", "react", "node.js", "mongodb",
    "mysql", "postgresql", "sqlite", "git", "github", "docker", "kubernetes",
    "aws", "azure", "gcp", "linux", "excel", "power bi", "tableau",
    "data structures", "algorithms", "dbms", "operating systems",
    "computer networks", "oop", "object oriented programming",
    "statistics", "probability", "matplotlib", "seaborn", "opencv",
    "rest api", "api development", "agile", "data analysis",
    "big data", "hadoop", "spark", "r programming", "matlab",
]


class ResumeAnalysisError(Exception):
    """Custom exception raised for resume processing failures."""
    pass


def extract_text_from_pdf(uploaded_file) -> str:
    """
    Extract raw text from an uploaded PDF file object (Streamlit UploadedFile).
    Raises ResumeAnalysisError with a user-friendly message on failure.
    """
    if uploaded_file is None:
        raise ResumeAnalysisError("No resume file was provided.")

    try:
        reader = PyPDF2.PdfReader(uploaded_file)
    except Exception:
        raise ResumeAnalysisError(
            "This file could not be read as a valid PDF. Please upload a valid, non-corrupted PDF file."
        )

    if len(reader.pages) == 0:
        raise ResumeAnalysisError("The uploaded PDF has no readable pages.")

    text_parts = []
    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        except Exception:
            # Skip unreadable pages but keep going
            continue

    full_text = "\n".join(text_parts).strip()

    if not full_text:
        raise ResumeAnalysisError(
            "No extractable text was found in this PDF. It may be a scanned image; "
            "please upload a text-based PDF resume."
        )

    return full_text


def extract_skills(resume_text: str, skills_db=None):
    """
    Extract skills mentioned in the resume text via dictionary/keyword matching.
    Returns a sorted list of unique matched skills.
    """
    if not resume_text:
        return []

    vocabulary = skills_db if skills_db is not None else SKILLS_DB
    cleaned = clean_text(resume_text)

    found = set()
    for skill in vocabulary:
        skill_clean = clean_text(skill)
        if skill_clean and skill_clean in cleaned:
            found.add(skill)

    return sorted(found)


def analyze_resume(uploaded_file):
    """
    Full pipeline: extract text -> extract skills.
    Returns a dict: {"text": ..., "skills": [...]}
    Raises ResumeAnalysisError on any failure (caught by the calling page).
    """
    text = extract_text_from_pdf(uploaded_file)
    skills = extract_skills(text)
    return {"text": text, "skills": skills}
