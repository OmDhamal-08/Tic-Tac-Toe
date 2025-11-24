import sqlite3
from contextlib import contextmanager

DB_NAME = "game.db"


def connect_db():
    """Return a new sqlite3 connection to the shared database."""
    return sqlite3.connect(DB_NAME)


def ensure_users_table():
    """Create the users table if it does not already exist."""
    with connect_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                total_games INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0
            )
            """
        )


@contextmanager
def db_cursor():
    """Context manager that yields a cursor and commits automatically."""
    with connect_db() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        finally:
            cursor.close()


# Ensure schema exists as soon as the module is imported.
ensure_users_table()

