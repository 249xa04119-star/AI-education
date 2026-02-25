import sqlite3

def init_db():
    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            name TEXT,
            class TEXT,
            subject TEXT,
            score INTEGER,
            risk TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(name, class_name, subject, score, risk):
    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("INSERT INTO results VALUES (?, ?, ?, ?, ?)",
              (name, class_name, subject, score, risk))
    conn.commit()
    conn.close()

def fetch_results():
    conn = sqlite3.connect("student_data.db")
    c = conn.cursor()
    c.execute("SELECT * FROM results")
    data = c.fetchall()
    conn.close()
    return data
