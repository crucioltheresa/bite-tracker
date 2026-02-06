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

        return self._restaurant_repo.filter_by_country(country.strip())

    def update_restaurant(
            self,
            restaurant_id: int,
            name: str,
            location: str,
            country: str,
            price_range: int,
            cuisine_type: Optional[str] = None,
            phone: Optional[str] = None,
            website: Optional[str] = None,
            social_media: Optional[str] = None
            ) -> Restaurant:
        """
        Update an existing restaurant

        Business rules:
        - Restaurant must exist
        - All validation is handled by the Restaurant model

        Args:
            restaurant_id: ID of restaurant to update
            name: Restaurant name
            location: Physical address or area
            country: Country where restaurant is located
            price_range: Price category (1-4)
            cuisine_type: Type of cuisine (optional)
            phone: Contact phone number (optional)
            website: Restaurant website URL (optional)
            social_media: Social media profile URL (optional)

        Returns:
            Updated Restaurant object

        Raises:
            NotFoundError: If restaurant does not exist
            ValidationError: If any updated value is invalid
            RepositoryError: If database operation fails
        """
        # Check if restaurant exists
        existing = self._restaurant_repo.get_by_id(restaurant_id)
        if existing is None:
            raise NotFoundError(f"Restaurant with ID {restaurant_id} not found")

        # Create updated restaurant object (validation happens in __post_init__)
        updated_restaurant = Restaurant(
            id=restaurant_id,
            name=name,
            location=location,
            country=country,
            price_range=price_range,
            cuisine_type=cuisine_type,
            phone=phone,
            website=website,
            social_media=social_media
        )

        # Persist updates to database
        success = self._restaurant_repo.update(updated_restaurant)

        if not success:
            raise NotFoundError(f"restaurant with ID {restaurant_id} not found")

        return updated_restaurant

    def delete_restaurant(self, restaurant_id: int) -> None:
        """
        Delete a restaurant.

        Business rules:
        - Restaurant must exist
        - Cannot delete restaurant if it has an associated visit
        (user must delete visit first)

        Args:
            restaurant_id: ID of restaurant to delete

        Raises:
            NotFoundError: If restaurant doesn't exist
            BusinessRuleViolationError: If restaurant has a visit
            RepositoryError: If database operation fails
        """
        # Verify restaurant exists
        restaurant = self._restaurant_repo.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError(f"Restaurant with ID {restaurant_id} not found")

        # Business rule: Check if restaurant has a visit
        visit = self._visit_repo.get_by_restaurant_id(restaurant_id)
        if visit is not None:
            raise BusinessRuleViolationError(
                f"Cannot delete restaurant '{restaurant.name}'. "
                f"Please delete the associated visit first."
            )

        # Safe to delete
        success = self._restaurant_repo.delete(restaurant_id)

        if not success:
            raise NotFoundError(f"Restaurant with ID {restaurant_id} not found")
