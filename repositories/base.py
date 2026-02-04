"""
Abstract base class for repositories.
Defines the interface for repository implementations.
Allows service layers t depend on abstractions rather
than concrete implementations.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from models import Restaurant, Visit


class RestaurantRepository(ABC):
    """
    Abstract base class for restaurant data access
    Defines the interface for repository implementations.
    """

    @abstractmethod
    def add(self, restaurant: Restaurant) -> Restaurant:
        """
        Add a new restaurant to the data store.
        Args:
            restaurant: Restaurant object (ID will be ignored/assigned).
        Returns:
            Restaurant object with assigned ID
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """
        Retrieve a restaurant by its ID.
        Args:
            restaurant_id: Unique identifier
        Returns:
            Restaurant object if found, None otherwise
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Restaurant]:
        """
        Retrieve all restaurants.
        Returns:
            List of all Restaurant objects (empty list if none exist)
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def update(self, restaurant: Restaurant) -> bool:
        """
        Update an existing restaurant.
        Args:
            restaurant: Restaurant object with ID set
        Returns:
            True if updated successfully, False if not found
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def delete(self, restaurant_id: int) -> bool:
        """
        Delete a restaurant by ID.
        Args:
            restaurant_id: Unique identifier
        Returns:
            True if deleted successfully, False if not found
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Restaurant]:
        """
        Search for restaurants by partial name match.
        Args:
            name: Search term
        Returns:
            List of matching restaurants (empty if no matches)
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def filter_by_country(self, country: str) -> List[Restaurant]:
        """
        Filter restaurants by country.
        Args:
            country: Country name
        Returns:
            List of restaurants in that country (empty if none)
        Raises:
            RepositoryError: If the operation fails
        """
        pass


class VisitRepository(ABC):
    """
    Abstract base class for visit data access
    Defines the interface for repository implementations.
    """

    @abstractmethod
    def add(self, visit: Visit) -> Visit:
        """
        Add a new visit to the data store.
        Args:
            visit: Visit object (id will be ignored/assigned)
        Returns:
            Visit object with assigned ID
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_by_id(self, visit_id: int) -> Optional[Visit]:
        """
        Retrieve a visit by its ID.
        Args:
            visit_id: Unique identifier
        Returns:
            Visit object if found, None otherwise
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_by_restaurant_id(self, restaurant_id: int) -> Optional[Visit]:
        """
        Retrieve the visit for a specific restaurant.
        Args:
            restaurant_id: ID of the restaurant
        Returns:
            Visit object if found, None otherwise
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Visit]:
        """
        Retrieve all visits.
        Returns:
            List of all Visit objects (empty list if none exist)
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def update(self, visit: Visit) -> bool:
        """
        Update an existing visit.
        Args:
            visit: Visit object with ID set
        Returns:
            True if updated successfully, False if not found
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def delete(self, visit_id: int) -> bool:
        """
        Delete a visit by ID.
        Args:
            visit_id: Unique identifier
        Returns:
            True if deleted successfully, False if not found
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def delete_by_restaurant_id(self, restaurant_id: int) -> bool:
        """
        Delete the visit associated with a restaurant.
        Args:
            restaurant_id: ID of the restaurant
        Returns:
            True if deleted successfully, False if not found
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def filter_by_meal_type(self, meal_type: str) -> List[Visit]:
        """
        Filter visits by meal type.
        Args:
            meal_type: Meal type (e.g., "breakfast", "lunch", "dinner")
        Returns:
            List of visits matching that meal type (empty if none)
        Raises:
            RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def filter_by_rating(self, min_rating: int) -> List[Visit]:
        """
        Filter visits by minimum rating.
        Args:
            min_rating: Minimum rating (1-5)
        Returns:
            List of visits with rating >= min_rating (empty if none)
        Raises:
            RepositoryError: If the operation fails
        """
        pass
