"""
database/database.py

Handles all SQLite database operations for the AI Interview Assistant:
    - student profile storage
    - interview session storage
    - individual question/answer results
    - performance history retrieval

Uses only Python's built-in sqlite3 module (no external dependency).
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "interview_assistant.db")


def get_connection():
    """Create (if needed) and return a SQLite connection with row access by column name."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all required tables if they do not already exist."""
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                branch TEXT,
                created_at TEXT
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS resumes (
                resume_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                extracted_text TEXT,
                extracted_skills TEXT,
                uploaded_at TEXT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS interview_sessions (
                session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                category TEXT,
                difficulty TEXT,
                started_at TEXT,
                overall_score REAL,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS question_results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER,
                question_id TEXT,
                question TEXT,
                topic TEXT,
                user_answer TEXT,
                score REAL,
                feedback TEXT,
                FOREIGN KEY (session_id) REFERENCES interview_sessions(session_id)
            )
        """)

        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"[Database Error] Failed to initialize database: {e}")
        return False


def add_student(name, email="", branch=""):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO students (name, email, branch, created_at) VALUES (?, ?, ?, ?)",
            (name, email, branch, datetime.now().isoformat()),
        )
        conn.commit()
        student_id = cur.lastrowid
        conn.close()
        return student_id
    except sqlite3.Error as e:
        print(f"[Database Error] add_student: {e}")
        return None


def save_resume(student_id, extracted_text, extracted_skills):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO resumes (student_id, extracted_text, extracted_skills, uploaded_at) VALUES (?, ?, ?, ?)",
            (student_id, extracted_text, ",".join(extracted_skills), datetime.now().isoformat()),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"[Database Error] save_resume: {e}")
        return False


def create_session(student_id, category, difficulty):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO interview_sessions (student_id, category, difficulty, started_at, overall_score) VALUES (?, ?, ?, ?, ?)",
            (student_id, category, difficulty, datetime.now().isoformat(), 0.0),
        )
        conn.commit()
        session_id = cur.lastrowid
        conn.close()
        return session_id
    except sqlite3.Error as e:
        print(f"[Database Error] create_session: {e}")
        return None


def save_question_result(session_id, question_id, question, topic, user_answer, score, feedback):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """INSERT INTO question_results
               (session_id, question_id, question, topic, user_answer, score, feedback)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (session_id, question_id, question, topic, user_answer, score, feedback),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"[Database Error] save_question_result: {e}")
        return False


def update_session_score(session_id, overall_score):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE interview_sessions SET overall_score = ? WHERE session_id = ?",
            (overall_score, session_id),
        )
        conn.commit()
        conn.close()
        return True
    except sqlite3.Error as e:
        print(f"[Database Error] update_session_score: {e}")
        return False


def get_all_sessions(student_id=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        if student_id:
            cur.execute(
                "SELECT * FROM interview_sessions WHERE student_id = ? ORDER BY started_at DESC",
                (student_id,),
            )
        else:
            cur.execute("SELECT * FROM interview_sessions ORDER BY started_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print(f"[Database Error] get_all_sessions: {e}")
        return []


def get_session_results(session_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM question_results WHERE session_id = ?", (session_id,))
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print(f"[Database Error] get_session_results: {e}")
        return []


def get_weak_topics(student_id, threshold=50.0):
    """Return topics where the average score across all sessions is below the threshold."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT qr.topic, AVG(qr.score) as avg_score, COUNT(*) as attempts
            FROM question_results qr
            JOIN interview_sessions s ON qr.session_id = s.session_id
            WHERE s.student_id = ?
            GROUP BY qr.topic
            HAVING avg_score < ?
            ORDER BY avg_score ASC
            """,
            (student_id, threshold),
        )
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print(f"[Database Error] get_weak_topics: {e}")
        return []


def get_student(student_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
        row = cur.fetchone()
        conn.close()
        return dict(row) if row else None
    except sqlite3.Error as e:
        print(f"[Database Error] get_student: {e}")
        return None


def get_all_students():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except sqlite3.Error as e:
        print(f"[Database Error] get_all_students: {e}")
        return []
