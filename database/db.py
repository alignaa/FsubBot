import sqlite3
from threading import RLock

DB_PATH = "database.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS broadcast (
        bot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT
    )
''')
conn.commit()

INSERTION_LOCK = RLock()

def add_user(bot_id, user_id, user_name):
    with INSERTION_LOCK:
        cursor.execute("INSERT INTO broadcast (bot_id, user_id, user_name) VALUES (?, ?, ?)", (bot_id, user_id, user_name))
        conn.commit()

def full_userbase():
    cursor.execute("SELECT bot_id, user_id, user_name FROM broadcast")
    rows = cursor.fetchall()
    return rows

def del_user(bot_id):
    with INSERTION_LOCK:
        cursor.execute("DELETE FROM broadcast WHERE bot_id = ?", (bot_id,))
        conn.commit()
