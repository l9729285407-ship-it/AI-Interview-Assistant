"""
utils/text_processing.py

Core NLP preprocessing utilities used across the application.
This module implements the classic NLP pipeline:
    1. Lowercasing
    2. Tokenization
    3. Stop-word removal
    4. Lemmatization (light-weight, NLTK WordNet)
    5. Keyword extraction helpers

These functions are used by resume_analyzer.py and answer_evaluator.py.
"""

import re
import string

# Fallback minimal stopword list, used if NLTK (or its data) is unavailable.
_FALLBACK_STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "and", "or", "but", "if", "of", "at", "by", "for", "with", "about",
    "to", "from", "in", "on", "it", "this", "that", "as", "i", "you",
    "he", "she", "we", "they", "them", "his", "her", "its", "our", "do",
    "does", "did", "have", "has", "had", "will", "would", "can", "could",
    "should", "not", "no", "so", "than", "then", "there", "here", "what",
    "which", "who", "whom", "when", "where", "why", "how", "all", "any",
    "both", "each", "few", "more", "most", "other", "some", "such",
}

NLTK_AVAILABLE = True
try:
    import nltk

    # Download required NLTK data quietly (only happens once, then cached).
    for pkg in ["punkt", "punkt_tab", "stopwords", "wordnet", "omw-1.4"]:
        try:
            nltk.data.find(f"tokenizers/{pkg}") if "punkt" in pkg else nltk.data.find(f"corpora/{pkg}")
        except LookupError:
            try:
                nltk.download(pkg, quiet=True)
            except Exception:
                pass

    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import word_tokenize

    try:
        STOPWORDS = set(stopwords.words("english"))
    except Exception:
        STOPWORDS = _FALLBACK_STOPWORDS

    _lemmatizer = WordNetLemmatizer()
except Exception:
    # NLTK is not installed or its data could not be fetched (e.g. no internet
    # access). The app still works end-to-end using a lightweight fallback:
    # regex-based tokenization and a static stop-word list. Lemmatization is
    # skipped in this fallback mode.
    NLTK_AVAILABLE = False
    STOPWORDS = _FALLBACK_STOPWORDS
    _lemmatizer = None


def clean_text(text: str) -> str:
    """Lowercase, strip punctuation and extra whitespace."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str):
    """Tokenize cleaned text into words. Falls back to simple split if NLTK punkt is unavailable."""
    cleaned = clean_text(text)
    if not cleaned:
        return []
    if NLTK_AVAILABLE:
        try:
            return word_tokenize(cleaned)
        except Exception:
            return cleaned.split()
    return cleaned.split()


def remove_stopwords(tokens):
    """Remove common English stop-words from a token list."""
    return [t for t in tokens if t not in STOPWORDS and t not in string.punctuation and len(t) > 1]


def lemmatize(tokens):
    """Reduce words to their base/dictionary form (skipped if NLTK is unavailable)."""
    if not NLTK_AVAILABLE or _lemmatizer is None:
        return tokens
    try:
        return [_lemmatizer.lemmatize(t) for t in tokens]
    except Exception:
        return tokens


def preprocess(text: str):
    """
    Full NLP preprocessing pipeline.
    Returns a list of clean, stop-word-free, lemmatized tokens.
    """
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    tokens = lemmatize(tokens)
    return tokens


def preprocess_to_string(text: str) -> str:
    """Convenience wrapper that returns preprocessed text as a single string (for TF-IDF vectorizers)."""
    return " ".join(preprocess(text))


def extract_keywords(text: str, top_n: int = 10):
    """
    Simple frequency-based keyword extraction.
    This is a RULE-BASED technique (word frequency counting), not a trained ML model.
    """
    tokens = preprocess(text)
    freq = {}
    for tok in tokens:
        freq[tok] = freq.get(tok, 0) + 1
    sorted_tokens = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, _ in sorted_tokens[:top_n]]
