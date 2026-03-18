import os
import sqlite3
from config import DB_PATH


def get_connection() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            full_name TEXT,
            username TEXT,
            phone TEXT,
            branch TEXT NOT NULL,
            target_role TEXT NOT NULL,
            complaint_text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        '''
    )
    cur.execute("PRAGMA table_info(complaints)")
    columns = [row[1] for row in cur.fetchall()]
    if 'phone' not in columns:
        cur.execute("ALTER TABLE complaints ADD COLUMN phone TEXT")
    conn.commit()
    conn.close()


def add_complaint(user_id: int, full_name: str, username: str, phone: str, branch: str, target_role: str, complaint_text: str, created_at: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        INSERT INTO complaints (user_id, full_name, username, phone, branch, target_role, complaint_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (user_id, full_name, username, phone, branch, target_role, complaint_text, created_at),
    )
    conn.commit()
    complaint_id = cur.lastrowid
    conn.close()
    return complaint_id


def get_complaints_by_branch(branch: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT * FROM complaints WHERE branch = ? ORDER BY id DESC',
        (branch,),
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_branch_counts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        'SELECT branch, COUNT(*) AS total FROM complaints GROUP BY branch ORDER BY branch ASC'
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def get_total_complaints() -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM complaints')
    total = cur.fetchone()[0]
    conn.close()
    return total


def get_all_complaints():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM complaints ORDER BY id DESC')
    rows = cur.fetchall()
    conn.close()
    return rows
