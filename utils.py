
import sqlite3
import pandas as pd
from datetime import datetime
import random

DB_PATH = "kids_math_app.db"

def save_result(question, user_answer, correct_answer, is_correct):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            question TEXT,
            user_answer INTEGER,
            correct_answer INTEGER,
            is_correct INTEGER
        )
    """)
    cursor.execute("""
        INSERT INTO study_results (date, question, user_answer, correct_answer, is_correct)
        VALUES (?, ?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d"), question, user_answer, correct_answer, is_correct))
    conn.commit()
    conn.close()

def get_results():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT date, question, user_answer, correct_answer, is_correct FROM study_results", conn)
    conn.close()
    return df

def save_question(content):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            content TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO questions (date, content)
        VALUES (?, ?)
    """, (datetime.now().strftime("%Y-%m-%d"), content))
    conn.commit()
    conn.close()

def generate_question(category):
    if category == "たし算・ひき算":
        a, b = random.randint(10, 100), random.randint(1, 100)
        op = random.choice(["+", "-"])
        question = f"{a} {op} {b}"
        answer = eval(question)
    elif category == "かけ算・わり算":
        a, b = random.randint(2, 12), random.randint(1, 12)
        op = random.choice(["×", "÷"])
        if op == "×":
            question = f"{a} × {b}"
            answer = a * b
        else:
            a = a * b
            question = f"{a} ÷ {b}"
            answer = a // b
    elif category == "分数":
        a, b = random.randint(1, 9), random.randint(1, 9)
        c, d = random.randint(1, 9), random.randint(1, 9)
        question = f"{a}/{b} + {c}/{d}"
        answer = round(a / b + c / d, 2)
    else:
        question = "未対応カテゴリ"
        answer = 0
    return question, answer

def get_wrong_questions(limit=10):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("""
        SELECT question, correct_answer 
        FROM study_results 
        WHERE is_correct = 0 
        ORDER BY date DESC 
        LIMIT ?
    """, conn, params=(limit,))
    conn.close()
    return df

DB_PATH = "kids_math_app.db"

def get_all_study_results(limit=100):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        "SELECT * FROM study_results ORDER BY date DESC LIMIT ?",
        conn,
        params=(limit,)
    )
    conn.close()
    return df

def get_all_questions(limit=100):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        "SELECT * FROM questions ORDER BY date DESC LIMIT ?",
        conn,
        params=(limit,)
    )
    conn.close()
    return df
