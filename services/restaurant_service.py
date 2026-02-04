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
