import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_PATH = os.path.join(BASE_DIR, '..', 'data', 'estoque.db')
SCRIPT_PATH = os.path.join(BASE_DIR, '..', 'script', 'create_tables.sql')

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    if os.path.exists(SCRIPT_PATH):
        with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
            conn.commit()

    return conn
