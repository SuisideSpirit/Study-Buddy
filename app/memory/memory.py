import sqlite3
from pathlib import Path
from datetime import datetime

from config import SQLITE_DB_PATH
from app.utils.logger import logger


class StudyBuddyMemory:

    def __init__(self, db_path: str = SQLITE_DB_PATH):

        self.db_path = Path(db_path)

        # Make sure the parent directory exists
        self.db_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.init_db()

    def get_connection(self):

        return sqlite3.connect(
            self.db_path
        )

    def init_db(self):

        with self.get_connection() as connection:

            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS study_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    action_type TEXT NOT NULL,
                    target_name TEXT,
                    details TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

            connection.commit()

        logger.info("Memory database initialized")


    def add_message(self,session_id: str,role: str,content: str):

        with self.get_connection() as connection:
            connection.execute(
                """
                INSERT INTO chat_history
                (session_id, role, content)
                VALUES (?, ?, ?)
                """,
                (
                    session_id,
                    role,
                    content
                )
            )

            connection.commit()


    def get_history(self, session_id: str, limit: int = 5):

        with self.get_connection() as connection:

            cursor = connection.execute(
                """
                SELECT role, content
                FROM chat_history
                WHERE session_id = ?
                ORDER BY id DESC
                LIMIT ?
                """,
                (
                    session_id,
                    limit
                )
            )

            messages = cursor.fetchall()

        # Reverse because we retrieved newest first
        messages.reverse()

        return messages