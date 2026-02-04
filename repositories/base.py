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
