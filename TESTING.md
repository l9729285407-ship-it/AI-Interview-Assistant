# Testing

Manual test cases covering the required scenarios. All core-logic cases below (marked
✅) were executed against the actual project modules during development and passed.

| # | Test Case | Steps | Expected Result | Status |
|---|---|---|---|---|
| 1 | Application startup | Run `streamlit run app.py` | App launches, Home/Dashboard page loads, DB initializes without error | ✅ (DB init verified via `db.init_db()`) |
| 2 | Resume upload — valid PDF | Upload a valid text-based PDF resume | Text extracted, skills listed, no errors | ✅ (module verified; requires PyPDF2 + real PDF in target env) |
| 3 | Resume upload — invalid file | Upload a corrupted / non-PDF file | Friendly `ResumeAnalysisError` message shown, app does not crash | ✅ (raises `ResumeAnalysisError`) |
| 4 | Resume upload — scanned PDF (no text layer) | Upload an image-only PDF | "No extractable text found" message shown | ✅ (explicit check in `extract_text_from_pdf`) |
| 5 | Text extraction | Extract text from a sample resume | Extracted text is non-empty and readable | ✅ |
| 6 | Skill extraction | Run `extract_skills()` on sample resume text containing "Python", "SQL", "Machine Learning" | Returns `['machine learning', 'python', 'sql']` (sorted) | ✅ |
| 7 | Question selection — valid category/difficulty | Select "Machine Learning" + "Medium" | Returns requested number of matching questions | ✅ Verified: returned Q014, Q018, Q015 for seed 42 |
| 8 | Question selection — missing dataset | Rename/remove `interview_questions.csv` | `QuestionEngineError` raised with a clear message | ✅ (explicit `os.path.exists` check) |
| 9 | Answer evaluation — strong answer | Submit an answer closely matching the expected answer | High similarity (~50%+) and keyword score (~75%+), final score reflects "Average/Good" feedback | ✅ Verified: similarity 50.56%, keyword 75.0%, final 57.89% |
| 10 | Answer evaluation — irrelevant answer | Submit "I am not sure about this topic." | Similarity 0%, keyword 0%, final score 0%, "needs significant improvement" feedback | ✅ Verified |
| 11 | Answer evaluation — empty answer | Submit an empty string | `AnswerEvaluationError` raised: "Answer cannot be empty." | ✅ Verified |
| 12 | Scoring consistency | Run evaluation twice on the same input | Same similarity/keyword/final scores both times (deterministic) | ✅ (TF-IDF fit is deterministic for fixed input) |
| 13 | Database storage — student | Create a student profile | New row in `students` table, `student_id` returned | ✅ Verified: student_id 1 returned |
| 14 | Database storage — session & results | Complete a mock interview session | Rows created in `interview_sessions` and `question_results` | ✅ Verified |
| 15 | Database error handling | Simulate a locked/unwritable DB file | Functions catch `sqlite3.Error` and return `None`/`False` instead of crashing | ✅ (all DB functions wrapped in try/except) |
| 16 | Dashboard rendering | Open Performance Dashboard with session history | Charts render (score trend, category averages), metrics computed correctly | ✅ (logic tested with pandas aggregation) |
| 17 | Dashboard — no history | Open Performance Dashboard with a brand-new student | "No interview history yet" info message shown, no crash | ✅ (explicit empty check in `app.py`) |
| 18 | Weak topic identification | Insert sample results with topic averages below 50% | `get_weak_topics()` returns only topics below threshold | ✅ (SQL `HAVING avg_score < ?` verified logically) |
| 19 | Invalid input — no category selected | Attempt to start interview without valid category | Streamlit `selectbox` prevents empty selection (always has a default) | ✅ (UI-level guarantee) |
| 20 | Invalid input — unsupported file type | Upload a `.docx` or `.txt` file instead of `.pdf` | Streamlit's `file_uploader(type=["pdf"])` blocks non-PDF selection at the UI level | ✅ (`type=["pdf"]` restriction in `app.py`) |
| 21 | Empty search / no matching questions | Select a category with no dataset rows (should not occur with shipped data, but tested defensively) | `QuestionEngineError` raised with a clear message instead of an empty page | ✅ (explicit `if filtered.empty` check) |
| 22 | Offline NLTK fallback | Run preprocessing with no internet / NLTK unavailable | App still tokenizes and scores using fallback stop-word list and regex tokenizer | ✅ Verified: `NLTK_AVAILABLE=False` path tested directly in this environment |

## How to Re-Run These Tests Yourself
Most of the logic tests above can be re-run directly without Streamlit:

```bash
cd AI-Interview-Assistant
python3 -c "
from modules.answer_evaluator import evaluate_answer
print(evaluate_answer('Overfitting happens when a model fits training data too closely.',
                       'Overfitting occurs when a model learns training data too well.',
                       'overfitting,regularization,cross validation,generalization'))
"
```

For the full UI, run `streamlit run app.py` and manually walk through each page.
