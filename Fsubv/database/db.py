import sqlite3
from threading import RLock
from Fsubv.config import LOGGER
import os

DB_FOLDER = 'C:/sqlite3'
DB_FILE = 'fsub.db'
DB_PATH = os.path.join(DB_FOLDER, DB_FILE)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

LOGGER.info("Database connected successfully: %s", DB_PATH)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS broadcast (
        bot_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        user_name TEXT
    )
''')
conn.commit()

LOGGER.info("Table broadcast is ready or already exists")
INSERTION_LOCK = RLock()

def add_user(bot_id, user_id, user_name):
    with INSERTION_LOCK:
        try:
            cursor.execute("INSERT INTO broadcast (bot_id, user_id, user_name) VALUES (?, ?, ?)", (bot_id, user_id, user_name))
            conn.commit()
            LOGGER.info("User add: bot_id=%s, user_id=%s, user_name='%s'",bot_id, user_id, user_name)
        except sqlite3.IntegrityError:
            LOGGER.warning("User already exists: bot_id=%s, user_id=%s, user_name='%s'",bot_id, user_id, user_name)

def full_userbase():
    cursor.execute("SELECT bot_id, user_id, user_name FROM broadcast")
    rows = cursor.fetchall()
    return rows

def del_user(user_id):
    with INSERTION_LOCK:
        cursor.execute("DELETE FROM broadcast WHERE user_id = ?", (user_id,))
        conn.commit()
        LOGGER.info("User deleted: user_id=%s", user_id)
