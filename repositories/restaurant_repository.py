"""
SQLite implementation of the RestaurantRepository.
Handles all restaurant data persistence using SQLite database.
"""

import sqlite3
from pathlib import Path
from typing import List, Optional
from models import Restaurant
from exceptions import RepositoryError, NotFoundError
from repositories.base import RestaurantRepository


class SqliteRestaurantRepository(RestaurantRepository):
    """SQLite implementation of restaurant data access."""

    def __init__(self, db_path: str = "data/bite_tracker.db"):
        """Initialize repository and ensure database exists."""
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """ Create database file and restaurant table if they don't exist. """
        try:
            # Create data directory if it doesn't exist
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

            # Connect to database (creates file if doesn't exist)
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Create restaurants table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS restaurants (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    location TEXT NOT NULL,
                    country TEXT NOT NULL,
                    cuisine_type TEXT,
                    price_range INTEGER NOT NULL,
                    phone TEXT,
                    website TEXT,
                    social_media TEXT
                )
            """)

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to initialize database: {e}")
