import os
from contextlib import contextmanager
from dotenv import load_dotenv
from psycopg import Connection

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME", "sfmshop"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "1234")
}


@contextmanager
def get_connection():
    """Контекстный менеджер для подключения к БД"""
    conn = None
    try:
        conn = Connection.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Ошибка БД: {e}")
        raise
    finally:
        if conn:
            conn.close()