"""
app.py

AI-Based Interview Preparation Assistant Using Machine Learning and NLP
Main Streamlit application entry point.

Run with:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

from database import database as db
from modules.resume_analyzer import analyze_resume, ResumeAnalysisError
from modules.question_engine import (
    load_questions, get_categories, get_difficulties,
    select_questions, QuestionEngineError,
)
from modules.answer_evaluator import evaluate_answer, AnswerEvaluationError
from modules.recommendation import generate_recommendations

# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Interview Preparation Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# INIT DATABASE (idempotent, safe to call every run)
# ----------------------------------------------------------------------------
db_ready = db.init_db()

# ----------------------------------------------------------------------------
# SESSION STATE DEFAULTS
# ----------------------------------------------------------------------------
defaults = {
    "student_id": None,
    "student_name": None,
    "resume_text": None,
    "resume_skills": [],
    "current_questions": [],
    "current_index": 0,
    "current_session_id": None,
    "session_results": [],
    "quiz_category": None,
    "quiz_difficulty": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ----------------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------------
st.sidebar.title("🎯 AI Interview Assistant")

if st.session_state.student_name:
    st.sidebar.success(f"Logged in as: {st.session_state.student_name}")
else:
    st.sidebar.info("Please create a profile to get started.")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home / Dashboard",
        "👤 Student Profile",
        "📄 Resume Analyzer",
        "🎤 Mock Interview",
        "📊 Result Page",
        "📈 Performance Dashboard",
        "🕘 Interview History",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("B.Tech AI/ML Third Year Project")
st.sidebar.caption("ML/NLP techniques used: TF-IDF, Cosine Similarity, Tokenization, "
                    "Stop-word Removal, Lemmatization, Keyword Extraction")


# ----------------------------------------------------------------------------
# GUARD: database must be ready
# ----------------------------------------------------------------------------
if not db_ready:
    st.error("⚠️ Database could not be initialized. Please check file permissions and restart the app.")
    st.stop()


# ==============================================================================
# PAGE 1: HOME / DASHBOARD
# ==============================================================================
if page == "🏠 Home / Dashboard":
    st.title("🎯 AI-Based Interview Preparation Assistant")
    st.markdown("### Using Machine Learning and Natural Language Processing")

    st.markdown(
        """
        Welcome! This application helps you prepare for technical interviews by:
        - Analyzing your resume and extracting your technical skills
        - Letting you choose an interview category and difficulty
        - Evaluating your written answers using **TF-IDF + Cosine Similarity** (NLP/ML)
        - Giving you a score, detailed feedback, and weak-topic recommendations
        """
    )

    col1, col2, col3, col4 = st.columns(4)
    try:
        df = load_questions()
        total_questions = len(df)
        total_categories = df["category"].nunique()
    except QuestionEngineError as e:
        total_questions, total_categories = 0, 0
        st.warning(f"⚠️ {e}")

    all_sessions = db.get_all_sessions()
    total_sessions = len(all_sessions)
    avg_score = round(pd.Series([s["overall_score"] for s in all_sessions]).mean(), 2) if all_sessions else 0.0

    col1.metric("📚 Total Questions", total_questions)
    col2.metric("🗂️ Categories", total_categories)
    col3.metric("📝 Interview Sessions Completed", total_sessions)
    col4.metric("⭐ Average Score (All Time)", f"{avg_score}%")

    st.markdown("---")
    st.subheader("How the AI/ML works in this project")
    st.markdown(
        """
        | Step | Technique | Type |
        |---|---|---|
        | Resume skill extraction | Dictionary/keyword matching | Rule-based |
        | Text cleaning | Tokenization, stop-word removal, lemmatization | NLP preprocessing |
        | Answer scoring (core) | TF-IDF vectorization + Cosine Similarity | ML/NLP |
        | Keyword coverage scoring | Keyword set matching | Rule-based |
        | Weak-topic detection | Aggregated score averaging + threshold | Rule-based analytics |
        """
    )

    if not st.session_state.student_id:
        st.info("👉 Head to **Student Profile** to create your profile and get started.")


# ==============================================================================
# PAGE 2: STUDENT PROFILE
# ==============================================================================
elif page == "👤 Student Profile":
    st.title("👤 Student Profile")

    with st.form("profile_form"):
        name = st.text_input("Full Name *", value=st.session_state.student_name or "")
        email = st.text_input("Email")
        branch = st.text_input("Branch / Department", value="AI & ML")
        submitted = st.form_submit_button("Save Profile")

        if submitted:
            if not name.strip():
                st.error("⚠️ Name is required.")
            else:
                student_id = db.add_student(name.strip(), email.strip(), branch.strip())
                if student_id:
                    st.session_state.student_id = student_id
                    st.session_state.student_name = name.strip()
                    st.success(f"✅ Profile created successfully! Welcome, {name.strip()}.")
                else:
                    st.error("⚠️ Could not save profile. Please try again.")

    if st.session_state.student_id:
        st.markdown("---")
        st.subheader("Current Profile")
        student = db.get_student(st.session_state.student_id)
        if student:
            st.json(student)


# ==============================================================================
# PAGE 3: RESUME ANALYZER
# ==============================================================================
elif page == "📄 Resume Analyzer":
    st.title("📄 Resume Analyzer")

    if not st.session_state.student_id:
        st.warning("⚠️ Please create your Student Profile first.")
        st.stop()

    st.markdown("Upload your resume in **PDF format** to extract your skills automatically.")
    uploaded_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

    if uploaded_file is not None:
        if st.button("🔍 Analyze Resume"):
            with st.spinner("Extracting text and analyzing skills..."):
                try:
                    result = analyze_resume(uploaded_file)
                    st.session_state.resume_text = result["text"]
                    st.session_state.resume_skills = result["skills"]
                    db.save_resume(st.session_state.student_id, result["text"], result["skills"])
                    st.success("✅ Resume analyzed successfully!")
                except ResumeAnalysisError as e:
                    st.error(f"⚠️ {e}")
                except Exception as e:
                    st.error(f"⚠️ An unexpected error occurred while processing the resume: {e}")

    if st.session_state.resume_skills:
        st.markdown("---")
        st.subheader("🛠️ Extracted Skills")
        st.write(", ".join(st.session_state.resume_skills) if st.session_state.resume_skills
                  else "No known skills detected.")

        st.subheader("📃 Extracted Resume Text (preview)")
        with st.expander("View extracted text"):
            st.text(st.session_state.resume_text[:3000])


# ==============================================================================
# PAGE 4: MOCK INTERVIEW
# ==============================================================================
elif page == "🎤 Mock Interview":
    st.title("🎤 Mock Interview")

    if not st.session_state.student_id:
        st.warning("⚠️ Please create your Student Profile first.")
        st.stop()

    if not st.session_state.current_questions:
        st.subheader("Step 1: Configure Your Mock Interview")

        try:
            categories = get_categories()
        except QuestionEngineError as e:
            st.error(f"⚠️ {e}")
            st.stop()

        col1, col2, col3 = st.columns(3)
        with col1:
            category = st.selectbox("Interview Category", categories)
        with col2:
            difficulty = st.selectbox("Difficulty", get_difficulties())
        with col3:
            num_q = st.slider("Number of Questions", min_value=3, max_value=10, value=5)

        if st.button("🚀 Start Mock Interview"):
            try:
                questions = select_questions(category, difficulty, num_questions=num_q)
                session_id = db.create_session(st.session_state.student_id, category, difficulty)
                if session_id is None:
                    st.error("⚠️ Could not start a new interview session. Please try again.")
                    st.stop()
                st.session_state.current_questions = questions
                st.session_state.current_index = 0
                st.session_state.current_session_id = session_id
                st.session_state.session_results = []
                st.session_state.quiz_category = category
                st.session_state.quiz_difficulty = difficulty
                st.rerun()
            except QuestionEngineError as e:
                st.error(f"⚠️ {e}")

    else:
        questions = st.session_state.current_questions
        idx = st.session_state.current_index
        total = len(questions)

        if idx < total:
            q = questions[idx]
            st.progress((idx) / total)
            st.caption(f"Question {idx + 1} of {total} | Category: {q['category']} | Topic: {q['topic']} | Difficulty: {q['difficulty']}")
            st.subheader(q["question"])

            answer_key = f"answer_{idx}"
            user_answer = st.text_area("Your Answer", key=answer_key, height=180)

            if st.button("Submit Answer ➡️"):
                try:
                    eval_result = evaluate_answer(
                        user_answer, q["expected_answer"], q["keywords"]
                    )
                    db.save_question_result(
                        st.session_state.current_session_id,
                        q["question_id"], q["question"], q["topic"],
                        user_answer, eval_result["final_score"], eval_result["feedback"],
                    )
                    st.session_state.session_results.append({
                        "question": q["question"],
                        "topic": q["topic"],
                        "user_answer": user_answer,
                        **eval_result,
                    })
                    st.session_state.current_index += 1
                    st.rerun()
                except AnswerEvaluationError as e:
                    st.error(f"⚠️ {e}")
                except Exception as e:
                    st.error(f"⚠️ An unexpected error occurred while evaluating your answer: {e}")
        else:
            # Interview finished
            scores = [r["final_score"] for r in st.session_state.session_results]
            overall = round(sum(scores) / len(scores), 2) if scores else 0.0
            db.update_session_score(st.session_state.current_session_id, overall)

            st.success(f"🎉 Interview Completed! Overall Score: {overall}%")
            st.info("👉 Visit the **Result Page** to see detailed feedback, or **Performance Dashboard** for analytics.")

            if st.button("🔄 Start a New Interview"):
                st.session_state.current_questions = []
                st.session_state.current_index = 0
                st.session_state.current_session_id = None
                st.session_state.session_results = []
                st.rerun()


# ==============================================================================
# PAGE 5: RESULT PAGE
# ==============================================================================
elif page == "📊 Result Page":
    st.title("📊 Result Page")

    if not st.session_state.session_results:
        st.info("No completed interview results yet in this session. Complete a Mock Interview first.")
    else:
        scores = [r["final_score"] for r in st.session_state.session_results]
        overall = round(sum(scores) / len(scores), 2)

        st.metric("Overall Score", f"{overall}%")
        st.markdown(f"**Category:** {st.session_state.quiz_category}  |  **Difficulty:** {st.session_state.quiz_difficulty}")

        st.markdown("---")
        for i, r in enumerate(st.session_state.session_results, start=1):
            with st.expander(f"Q{i}: {r['question'][:80]}..."):
                st.write(f"**Topic:** {r['topic']}")
                st.write(f"**Your Answer:** {r['user_answer']}")
                st.write(f"**Similarity Score (TF-IDF + Cosine):** {r['similarity_score']}%")
                st.write(f"**Keyword Match Score:** {r['keyword_score']}%")
                st.write(f"**Final Score:** {r['final_score']}%")
                st.info(r["feedback"])

        st.markdown("---")
        st.subheader("📉 Weak Topic Identification")
        topic_scores = {}
        for r in st.session_state.session_results:
            topic_scores.setdefault(r["topic"], []).append(r["final_score"])
        weak_topics = [t for t, s in topic_scores.items() if sum(s) / len(s) < 50]

        if weak_topics:
            st.warning(f"Topics to review: {', '.join(weak_topics)}")
        else:
            st.success("No weak topics detected in this session. Great performance!")


# ==============================================================================
# PAGE 6: PERFORMANCE DASHBOARD
# ==============================================================================
elif page == "📈 Performance Dashboard":
    st.title("📈 Performance Dashboard")

    if not st.session_state.student_id:
        st.warning("⚠️ Please create your Student Profile first.")
        st.stop()

    sessions = db.get_all_sessions(st.session_state.student_id)

    if not sessions:
        st.info("No interview history yet. Complete a Mock Interview to see your dashboard.")
    else:
        df_sessions = pd.DataFrame(sessions)
        df_sessions["started_at"] = pd.to_datetime(df_sessions["started_at"])
        df_sessions = df_sessions.sort_values("started_at")

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Sessions", len(df_sessions))
        col2.metric("Average Score", f"{round(df_sessions['overall_score'].mean(), 2)}%")
        col3.metric("Best Score", f"{round(df_sessions['overall_score'].max(), 2)}%")

        st.markdown("---")
        st.subheader("Score Trend Over Time")
        fig = px.line(df_sessions, x="started_at", y="overall_score", markers=True,
                      labels={"started_at": "Date", "overall_score": "Score (%)"})
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Average Score by Category")
        fig2 = px.bar(
            df_sessions.groupby("category", as_index=False)["overall_score"].mean(),
            x="category", y="overall_score",
            labels={"category": "Category", "overall_score": "Average Score (%)"},
        )
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown("---")
        st.subheader("💡 Personalized Recommendations")
        recommendations = generate_recommendations(st.session_state.student_id)
        for rec in recommendations:
            st.write(f"**{rec['topic']}**: {rec['message']}")


# ==============================================================================
# PAGE 7: INTERVIEW HISTORY
# ==============================================================================
elif page == "🕘 Interview History":
    st.title("🕘 Interview History")

    if not st.session_state.student_id:
        st.warning("⚠️ Please create your Student Profile first.")
        st.stop()

    sessions = db.get_all_sessions(st.session_state.student_id)

    if not sessions:
        st.info("No past interview sessions found.")
    else:
        for s in sessions:
            with st.expander(f"Session #{s['session_id']} — {s['category']} ({s['difficulty']}) — Score: {round(s['overall_score'], 2)}%"):
                st.write(f"**Started at:** {s['started_at']}")
                results = db.get_session_results(s["session_id"])
                if results:
                    df_results = pd.DataFrame(results)[["question", "topic", "score", "feedback"]]
                    st.dataframe(df_results, use_container_width=True)
                else:
                    st.write("No question-level results found for this session.")
