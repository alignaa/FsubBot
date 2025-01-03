from Fsubv.config import LOGGER
import sqlite3
import os

db_folder = 'C:/sqlite3'
db_file = 'fsub.db'
db_path = os.path.join(db_folder, db_file)

os.makedirs(db_folder, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.execute('PRAGMA foreign_keys = ON;')
    cursor = conn.cursor()
    return conn, cursor

def close_db(conn, cursor):
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

        print("Tabel berhasil dibuat.")
    
    except sqlite3.Error as e:
        print(f"Terjadi kesalahan saat membuat tabel: {e}")
    
    finally:
        close_db(conn, cursor)

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