"""
SQLite implementation of the VisitRepository.
Handles all visit data persistence using SQLite database.
Manages the relationship between visits and restaurants.
"""

import sqlite3
from pathlib import Path
from datetime import date
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

    def _row_to_visit(self, row: sqlite3.Row) -> Visit:
        """ Convert database row to a Visit object. """
        return Visit(
            id=row['id'],
            restaurant_id=row['restaurant_id'],
            visit_date=date.fromisoformat(row['visit_date']),
            rating=row['rating'],
            meal_type=row['meal_type'],
            service_rating=row['service_rating'],
            dishes_ordered=row['dishes_ordered'],
            recommended_dishes=row['recommended_dishes'],
            beverage_ordered=row['beverage_ordered'],
            total_cost=row['total_cost'],
            notes=row['notes'],
            would_return=bool(row['would_return'])
        )

    def add(self, visit: Visit) -> Visit:
        """ Add a new visit to the database.
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Enable foreign key constraints
            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("""
                        INSERT INTO visits (
                    restaurant_id, visit_date, rating, meal_type,
                    service_rating, dishes_ordered, recommended_dishes,
                    beverage_ordered, total_cost, notes, would_return
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                visit.restaurant_id,
                visit.visit_date,
                visit.rating,
                visit.meal_type,
                visit.service_rating,
                visit.dishes_ordered,
                visit.recommended_dishes,
                visit.beverage_ordered,
                visit.total_cost,
                visit.notes,
                1 if visit.would_return else 0
            ))

            visit_id = cursor.lastrowid

            conn.commit()
            conn.close()

            # Return new Visit object with ID
            return Visit(
                id=visit_id,
                restaurant_id=visit.restaurant_id,
                visit_date=visit.visit_date,
                rating=visit.rating,
                meal_type=visit.meal_type,
                service_rating=visit.service_rating,
                dishes_ordered=visit.dishes_ordered,
                recommended_dishes=visit.recommended_dishes,
                beverage_ordered=visit.beverage_ordered,
                total_cost=visit.total_cost,
                notes=visit.notes,
                would_return=visit.would_return
            )

        except sqlite3.IntegrityError as e:
            # Foreign key violation or other constraint error
            raise RepositoryError(f"Failed to add visit: Invalid restaurant_id or constraint violation ({e})")
        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to add visit: {e}")

    def get_by_id(self, visit_id: int) -> Optional[Visit]:
        """
        Retrieve a visit by its ID.
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM visits WHERE id = ?", (visit_id,))
            row = cursor.fetchone()

            conn.close()

            if row is None:
                return None

            return self._row_to_visit(row)

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to get visit: {e}")

    def get_by_restaurant_id(self, restaurant_id: int) -> Optional[Visit]:
        """
        Retrieve the visit for a specific restaurant.
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.rowfactory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM visits WHERE restaurant_id = ?", (restaurant_id,))

            row = cursor.fetchone()

            conn.close()

            if row is None:
                return None

            return self._row_to_visit(row)

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to get visit: {e}")

    def get_all(self) -> List[Visit]:
        """
        Retrieve all visits.
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM visits order by visit_date DESC")
            rows = cursor.fetchall()

            conn.close()

            return [self._row_to_visit(row) for row in rows]

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to get visits: {e}")
