"""
Restaurant Service layer
Handles business logic ans orchestration for restaurant related operations
Sits between the CLI layer and repository layer
"""

from typing import List, Optional
from models import Restaurant
from repositories import RestaurantRepository, VisitRepository
from exceptions import ValidationError, BusinessRuleViolationError, NotFoundError


class RestaurantService:
    """
    Service for managing restaurant business logic.
    Depends on repository abstractions, not concrete implementations.
    Enforces business rules and operations.
    """

    def __init__(self, restaurant_repo: RestaurantRepository, visit_repo: VisitRepository):
        """Initialize with repository dependencies."""
        self._restaurant_repo = restaurant_repo
        self._visit_repo = visit_repo

    def create_restaurant(
            self, name: str,
            location: str,
            country: str,
            price_range: int,
            cuisine_type: Optional[str] = None,
            phone: Optional[str] = None,
            website: Optional[str] = None,
            social_media: Optional[str] = None
            ) -> Restaurant:
        """
        Create a new restaurant

        Business rules:
        - All validation is handled by the Restaurant model
        - Name, location, country, and price_range are required

        Args:
            name: Restaurant name
            location: Physical address or area
            country: Country where restaurant is located
            price_range: Price category (1-4)
            cuisine_type: Type of cuisine (optional)
            phone: Contact phone number (optional)
            website: Restaurant website URL (optional)
            social_media: Social media profile URL (optional)

        Returns:
            Created Restaurant object with assigned ID

        Raises:
            ValidationError: If any input is invalid
            RepositoryError: If database operation fails
        """
        # Create a restaurant object (validation happens in __post_init__)
        restaurant = Restaurant(
            name=name,
            location=location,
            country=country,
            price_range=price_range,
            cuisine_type=cuisine_type,
            phone=phone,
            website=website,
            social_media=social_media
        )

        # Persist to database
        return self._restaurant_repo.add(restaurant)

    def get_restaurant(self, restaurant_id: int) -> Restaurant:
        """
        Get a restaurant by ID.
        Raises: NotFoundError: If no restaurant with the given ID exists
        RepositoryError: If database operation fails
        """
        restaurant = self._restaurant_repo.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError(f"Restaurant with ID {restaurant_id} not found")

        return restaurant

    def get_all_restaurants(self) -> List[Restaurant]:
        """
        Get all restaurants.
        Raises: RepositoryError: If database operation fails
        """
        return self._restaurant_repo.get_all()

    def search_restaurants(self, name: str) -> List[Restaurant]:
        """
        Search restaurant by partial name match
        Raises: ValidationError: If search term is empty
        RepositoryError: If database operation fails
        """
        if not name or not name.strip():
            raise ValidationError("Search term cannot be empty")

        return self._restaurant_repo.search_by_name(name.strip())

    def get_restaurants_by_country(self, country: str) -> List[Restaurant]:
        """
        Filter restaurants by country
        Raises: ValidationError: If country is empty
        RepositoryError: If database operation fails
        """
        if not country or not country.strip():
            raise ValidationError("Country cannot be empty")

        return self._restaurant_repo.get_by_country(country.strip())

