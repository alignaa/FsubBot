from Fsubv.config import LOGGER
import os
import sqlite3
from threading import RLock
from contextlib import contextmanager
import logging

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

# Konfigurasi database
DB_FOLDER = 'C:/sqlite3'
DB_FILE = 'fsub.db'
DB_PATH = os.path.join(DB_FOLDER, DB_FILE)

os.makedirs(DB_FOLDER, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    conn.execute('PRAGMA foreign_keys = ON;')  # Menjamin foreign key aktif
    return conn, cursor

def close_db_connection(conn, cursor):
    cursor.close()
    conn.close()

def create_table():
    conn, cursor = get_db_connection()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS broadcast (
                bot_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                user_name TEXT
            )
        ''')
        conn.commit()
        LOGGER.info("Table 'broadcast' is ready or already exists")
    finally:
        cursor.close()
        conn.close()

def add_user(bot_id, user_id, user_name):
    conn, cursor = get_db_connection()
    try:
        cursor.execute(
            "INSERT INTO broadcast (bot_id, user_id, user_name) VALUES (?, ?, ?)", 
            (bot_id, user_id, user_name)
        )
        conn.commit()
        LOGGER.info("User added: bot_id=%s, user_id=%s, user_name='%s'", bot_id, user_id, user_name)
    except sqlite3.IntegrityError:
        LOGGER.warning("User already exists: bot_id=%s, user_id=%s, user_name='%s'", bot_id, user_id, user_name)
    finally:
        cursor.close()
        conn.close()

def full_userbase():
    conn, cursor = get_db_connection()
    try:
        cursor.execute("SELECT bot_id, user_id, user_name FROM broadcast")
        rows = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()
    return rows

def del_user(user_id):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("DELETE FROM broadcast WHERE user_id = ?", (user_id,))
        conn.commit()
        LOGGER.info("User deleted: user_id=%s", user_id)
    finally:
        cursor.close()
        conn.close()

create_table()