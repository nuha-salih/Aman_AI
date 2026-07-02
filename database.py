import sqlite3

DATABASE_NAME = "aman_ai.db"


def create_database():

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS fraud_logs (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        input_type TEXT,
        content TEXT,
        risk_score INTEGER,
        confidence_score INTEGER,
        risk_level TEXT,
        scam_detected BOOLEAN,
        summary TEXT

    )
    """)

    conn.commit()
    conn.close()


# ---------------- SAVE ----------------

def save_analysis(
    input_type,
    content,
    risk_score,
    confidence_score,
    risk_level,
    scam_detected,
    summary
):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO fraud_logs (
        input_type,
        content,
        risk_score,
        confidence_score,
        risk_level,
        scam_detected,
        summary
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        input_type,
        content,
        risk_score,
        confidence_score,
        risk_level,
        scam_detected,
        summary
    ))

    conn.commit()
    conn.close()


# ---------------- GET LOGS ----------------

def get_all_logs(limit=50):

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, timestamp, input_type, content,
               risk_score, confidence_score, risk_level,
               scam_detected, summary
        FROM fraud_logs
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()
    conn.close()

    return rows