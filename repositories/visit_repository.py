"""
SQLite implementation of the VisitRepository.
Handles all visit data persistence using SQLite database.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional
from models import Visit
from exceptions import RepositoryError, NotFoundError
from repositories.base import VisitRepository


class SqliteVisitRepository(VisitRepository):
    """SQlite implementation of visit data access."""

    def __init__(self, db_path: str = "data/bite_tracker.db"):
        """Initialize repository and ensure database exists."""
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """ Create database file and visit table if they don't exist. """
        try:
            # Create data directory if it doesn't exist
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

            # Connect to database (creates file if doesn't exist)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create visits table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        restaurant_id INTEGER NOT NULL,
                        visit_date TEXT NOT NULL,
                        rating INTEGER,
                        comments TEXT,
                        FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
                    )
            """)

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to initialize database: {e}")
