"""
SQLite implementation of the VisitRepository.
Handles all visit data persistence using SQLite database.
Manages the relationship between visits and restaurants.
"""

import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from models import Visit
from exceptions import RepositoryError
from repositories.base import VisitRepository


class SqliteVisitRepository(VisitRepository):
    """SQlite implementation of visit data access.
    Creates and manages visit table in an SQLite database.
    Enforces foreign key relationship with restaurants table.
    """

    def __init__(self, db_path: str = "data/bite_tracker.db"):
        """Initialize repository and ensure database exists."""
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """ Create visit table if it doesn't exist.
        Enables foreign key constraints to maintain referential integrity.
        """
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = ON;")

            # Create visits table with foreign key to restaurants
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    restaurant_id INTEGER NOT NULL,
                    visit_date DATE NOT NULL,
                    rating INTEGER NOT NULL,
                    meal_type TEXT NOT NULL,
                    service_rating INTEGER,
                    dishes_ordered TEXT,
                    recommended_dishes TEXT,
                    beverage_ordered TEXT,
                    total_cost REAL,
                    notes TEXT,
                    would_return INTEGER NOT NULL DEFAULT 1,
                    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
                        ON DELETE CASCADE
                    )
            """)

            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to initialize database: {e}")
