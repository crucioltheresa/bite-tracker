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

    def _row_to_restaurant(self, row: sqlite3.Row) -> Restaurant:
        """ Convert a database row to a Restaurant object. """
        return Restaurant(
            id=row['id'],
            name=row['name'],
            location=row['location'],
            country=row['country'],
            cuisine_type=row['cuisine_type'],
            price_range=row['price_range'],
            phone=row['phone'],
            website=row['website'],
            social_media=row['social_media']
        )

    def add(self, restaurant: Restaurant) -> Restaurant:
        """
        Add a new restaurant to the database
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO restaurants (
                        name, location, country, cuisine_type,
                    price_range, phone, website, social_media
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                restaurant.name,
                restaurant.location,
                restaurant.country,
                restaurant.cuisine_type,
                restaurant.price_range,
                restaurant.phone,
                restaurant.website,
                restaurant.social_media
            ))

            # Get the auto-generated ID
            restaurant_id = cursor.lastrowid

            conn.commit()
            conn.close()

            # Return a new Restaurant object with the ID set
            return Restaurant(
                id=restaurant_id,
                name=restaurant.name,
                location=restaurant.location,
                country=restaurant.country,
                cuisine_type=restaurant.cuisine_type,
                price_range=restaurant.price_range,
                phone=restaurant.phone,
                website=restaurant.website,
                social_media=restaurant.social_media
            )

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to add restaurant: {e}")

    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """
        Retrieve a restaurant by its ID.
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Enable named column access
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM restaurants WHERE id = ?",
                (restaurant_id,)
            )
            row = cursor.fetchone()

            conn.close()

            if row is None:
                return None

            return self._row_to_restaurant(row)

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to get restaurant by ID: {e}")

    def get_all(self) -> List[Restaurant]:
        """
        Retrieve all restaurants.
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM restaurants ORDER BY name")
            rows = cursor.fetchall()

            conn.close()

            return [self._row_to_restaurant(row) for row in rows]

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to get all restaurants: {e}")

    def update(self, restaurant: Restaurant) -> bool:
        """
        Update an existing restaurant
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                UPDATE restaurants
                SET name = ?, location = ?, country = ?, cuisine_type = ?,
                    price_range = ?, phone = ?, website = ?, social_media = ?
                WHERE id = ?
            """, (
                restaurant.name,
                restaurant.location,
                restaurant.country,
                restaurant.cuisine_type,
                restaurant.price_range,
                restaurant.phone,
                restaurant.website,
                restaurant.social_media,
                restaurant.id
            ))

            rows_affected = cursor.rowcount

            conn.commit()
            conn.close()

            return rows_affected > 0

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to update restaurant: {e}")

    def delete(self, restaurant_id: int) -> bool:
        """
        Delete a restaurant ID
        Raises: RepositoryError: If database operation fails.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("DELETE FROM restaurants WHERE id = ?", (restaurant_id,))

            rows_affected = cursor.rowcount

            conn.commit()
            conn.close()

            return rows_affected > 0

        except sqlite3.Error as e:
            raise RepositoryError(f"Failed to delete restaurant: {e}")
