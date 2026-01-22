from database.connection import connection_factory
import sqlite3

def get_user(username):
    conn = connection_factory.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE Login = ?;", (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None
    return user

def register_user(username, password):
    conn = connection_factory.get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO User (Login, Password) VALUES (?, ?);", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()