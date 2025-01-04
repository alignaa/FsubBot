import os
import mysql.connector
import logging

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DB_HOST = 'localhost'
DB_USER = 'ranzxy'  # Ganti dengan username MySQL Anda
DB_PASSWORD = 'passranzy'  # Ganti dengan password MySQL Anda
DB_NAME = 'fsrans'  # Nama database MySQL yang ingin Anda gunakan

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_db_if_not_exists():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.close()

create_db_if_not_exists()

def create_table():
    conn, cursor = get_db_connection()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS broadcast (
                bot_id INT PRIMARY KEY AUTO_INCREMENT,
                user_id INT UNIQUE,
                user_name TEXT
            )
        ''')
        conn.commit()
        LOGGER.info("Tabel broadcast berhasil dibuat atau sudah ada.")
    except Exception as e:
        LOGGER.error(f"Error dalam membuat tabel: {e}")
    finally:
        cursor.close()
        conn.close()

def add_user(bot_id, user_id, user_name):
    conn, cursor = get_db_connection()
    try:
        cursor.execute(
            "INSERT INTO broadcast (bot_id, user_id, user_name) VALUES (%s, %s, %s)", 
            (bot_id, user_id, user_name)
        )
        conn.commit()
        LOGGER.info("User added: bot_id=%s, user_id=%s, user_name='%s'", bot_id, user_id, user_name)
    except mysql.connector.IntegrityError:
        LOGGER.warning("User already exists: bot_id=%s, user_id=%s, user_name='%s'", bot_id, user_id, user_name)
    finally:
        cursor.close()
        conn.close()

def full_userbase():
    conn, cursor = get_db_connection()
    try:
        cursor.execute("SELECT bot_id, user_id, user_name FROM broadcast")
        rows = cursor.fetchall()
        return rows
    finally:
        cursor.close()
        conn.close()

def del_user(user_id):
    conn, cursor = get_db_connection()
    try:
        cursor.execute("DELETE FROM broadcast WHERE user_id = %s", (user_id,))
        conn.commit()
        LOGGER.info("User deleted: user_id=%s", user_id)
    finally:
        cursor.close()
        conn.close()

create_table()