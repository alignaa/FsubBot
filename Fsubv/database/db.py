from Fsubv.config import LOGGER
import os
import sqlite3
from threading import RLock
from contextlib import contextmanager

# Konfigurasi database
DB_FOLDER = 'C:/sqlite3'
DB_FILE = 'fsub.db'
DB_PATH = os.path.join(DB_FOLDER, DB_FILE)

# Buat folder jika belum ada
os.makedirs(DB_FOLDER, exist_ok=True)

# Context manager untuk koneksi database
@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        conn.execute('PRAGMA foreign_keys = ON;')
        yield cursor
    finally:
        conn.commit()
        conn.close()

# Inisialisasi tabel
with get_db_connection() as cursor:
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS broadcast (
            bot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            user_name TEXT
        )
    ''')
    LOGGER.info("Table 'broadcast' is ready or already exists")

# Lock untuk operasi aman pada database
INSERTION_LOCK = RLock()

# Fungsi untuk menambah user
def add_user(bot_id, user_id, user_name):
    with INSERTION_LOCK:
        try:
            with get_db_connection() as cursor:
                cursor.execute(
                    "INSERT INTO broadcast (bot_id, user_id, user_name) VALUES (?, ?, ?)", 
                    (bot_id, user_id, user_name)
                )
            LOGGER.info("User added: bot_id=%s, user_id=%s, user_name='%s'", bot_id, user_id, user_name)
        except sqlite3.IntegrityError:
            LOGGER.warning("User already exists: bot_id=%s, user_id=%s, user_name='%s'", bot_id, user_id, user_name)

# Fungsi untuk mendapatkan semua data user
def full_userbase():
    with get_db_connection() as cursor:
        cursor.execute("SELECT bot_id, user_id, user_name FROM broadcast")
        rows = cursor.fetchall()
    return rows

# Fungsi untuk menghapus user berdasarkan user_id
def del_user(user_id):
    with INSERTION_LOCK:
        with get_db_connection() as cursor:
            cursor.execute("DELETE FROM broadcast WHERE user_id = ?", (user_id,))
        LOGGER.info("User deleted: user_id=%s", user_id)