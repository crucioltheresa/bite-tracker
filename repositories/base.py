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
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_by_id(self, restaurant_id: int) -> Optional[Restaurant]:
        """
        Retrieve a restaurant by its ID.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Restaurant]:
        """
        Retrieve all restaurants.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def update(self, restaurant: Restaurant) -> bool:
        """
        Update an existing restaurant.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def delete(self, restaurant_id: int) -> bool:
        """
        Delete a restaurant by ID.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def search_by_name(self, name: str) -> List[Restaurant]:
        """
        Search for restaurants by partial name match.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def filter_by_country(self, country: str) -> List[Restaurant]:
        """
        Filter restaurants by country.
        Raises: RepositoryError: If the operation fails
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
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_by_id(self, visit_id: int) -> Optional[Visit]:
        """
        Retrieve a visit by its ID.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_by_restaurant_id(self, restaurant_id: int) -> Optional[Visit]:
        """
        Retrieve the visit for a specific restaurant.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def get_all(self) -> List[Visit]:
        """
        Retrieve all visits.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def update(self, visit: Visit) -> bool:
        """
        Update an existing visit.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def delete(self, visit_id: int) -> bool:
        """
        Delete a visit by ID.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def delete_by_restaurant_id(self, restaurant_id: int) -> bool:
        """
        Delete the visit associated with a restaurant.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def filter_by_meal_type(self, meal_type: str) -> List[Visit]:
        """
        Filter visits by meal type.
        Raises: RepositoryError: If the operation fails
        """
        pass

    @abstractmethod
    def filter_by_rating(self, min_rating: int) -> List[Visit]:
        """
        Filter visits by minimum rating.
        Raises: RepositoryError: If the operation fails
        """
        pass
