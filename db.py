"""Database helpers for the guestbook app."""
import pymysql
from pymysql.cursors import DictCursor

from config import Config

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    content VARCHAR(1000) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""


def get_connection():
    """Open a new connection to the configured database."""
    return pymysql.connect(cursorclass=DictCursor, autocommit=True, **Config.db_kwargs())


def init_db():
    """Ensure the messages table exists."""
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE_SQL)


def add_message(name, content):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO messages (name, content) VALUES (%s, %s)",
                (name, content),
            )
            return cur.lastrowid


def get_messages(limit=100):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, content, created_at FROM messages "
                "ORDER BY id DESC LIMIT %s",
                (limit,),
            )
            return cur.fetchall()
