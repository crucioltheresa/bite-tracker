"""
Visit service layer.
Handles business logic and operations.
Enforces relationship rules between visits and restaurants.
"""

from typing import List, Optional
from datetime import date
from models import Visit
from repositories.base import RestaurantRepository, VisitRepository
from exceptions import ValidationError, BusinessRuleViolationError, NotFoundError


class VisitService:
    """
    Service for managing visit business logic.
    Enforces business rules related to the restaurant-visit relationship.
    """

    def __init__(
        self,
        visit_repo: VisitRepository,
        restaurant_repo: RestaurantRepository
    ):
        """
        Initialize service with repository dependencies.
        """
        self._visit_repo = visit_repo
        self._restaurant_repo = restaurant_repo

    def create_visit(
        self,
        restaurant_id: int,
        visit_date: date,
        rating: int,
        meal_type: str,
        service_rating: Optional[int] = None,
        dishes_ordered: Optional[str] = None,
        recommended_dishes: Optional[str] = None,
        beverage_ordered: Optional[str] = None,
        total_cost: Optional[float] = None,
        notes: Optional[str] = None,
        would_return: bool = True
    ) -> Visit:
        """
        Create a new visit.

        Business rules:
        - Restaurant must exist
        - Restaurant cannot already have a visit (1-to-1 relationship)
        - All validation is handled by the Visit model

        Args:
            restaurant_id: ID of the restaurant visited
            visit_date: Date of visit (first day of month)
            rating: Overall rating (1-5)
            meal_type: Type of meal (breakfast/lunch/dinner/brunch/other)
            service_rating: Service quality rating (1-5, optional)
            dishes_ordered: Comma-separated list of dishes (optional)
            recommended_dishes: Comma-separated recommended items (optional)
            beverage_ordered: Beverages consumed (optional)
            total_cost: Total amount spent (optional)
            notes: Personal notes (optional)
            would_return: Whether would visit again (default True)

        Returns:
            Created Visit object with assigned ID

        Raises:
            NotFoundError: If restaurant doesn't exist
            BusinessRuleViolationError: If restaurant already has a visit
            ValidationError: If any input is invalid
            RepositoryError: If database operation fails
        """
        # Business rule 1: Restaurant must exist
        restaurant = self._restaurant_repo.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError(
                f"Cannot create visit: Restaurant with ID {restaurant_id} not found."
            )

        # Business rule 2: Restaurant cannot already have a visit
        existing_visit = self._visit_repo.get_by_restaurant_id(restaurant_id)
        if existing_visit is not None:
            raise BusinessRuleViolationError(
                f"Restaurant '{restaurant.name}' already has a visit recorded."
                f"Please update the existing visit instead of creating a new one."
            )

        # Create Visit object
        visit = Visit(
            restaurant_id=restaurant_id,
            visit_date=visit_date,
            rating=rating,
            meal_type=meal_type,
            service_rating=service_rating,
            dishes_ordered=dishes_ordered,
            recommended_dishes=recommended_dishes,
            beverage_ordered=beverage_ordered,
            total_cost=total_cost,
            notes=notes,
            would_return=would_return
        )

        # Persist to database
        return self._visit_repo.add(visit)

    def get_visit(self, visit_id: int) -> Visit:
        """
        Get a visit by ID
        Raises: NotFoundError if visit doesn't exist
        RepositoryError if database operation fails
        """
        visit = self._visit_repo.get_by_id(visit_id)
        if visit is None:
            raise NotFoundError(f"Visit with ID {visit_id} not found.")
        return visit

    def get_visit_for_restaurant(self, restaurant_id: int) -> Optional[Visit]:
        """
        Get the visit for a specific restaurant.
        Raises: RepositoryError if database operation fails
        """
        return self._visit_repo.get_by_restaurant_id(restaurant_id)

    def get_all_visits(self) -> List[Visit]:
        """
        Get all visits.
        Raises: RepositoryError if database operation fails
        """
        return self._visit_repo.get_all()

    def get_top_rated_visits(self, min_rating: int = 5) -> List[Visit]:
        """
        Get visits with a minimum rating.
        Raises: RepositoryError if database operation fails
        """
        if not isinstance(min_rating, int) or min_rating not in [1, 2, 3, 4, 5]:
            raise ValidationError("Mininum rating must be between 1 and 5")

        return self._visit_repo.filter_by_rating(min_rating)

    def get_visit_by_meal_type(self, meal_type: str) -> List[Visit]:
        """
        Filter visits by meal type
        Raises: ValidationError if meal_type is invalid
        RepoditoryError if database operation fail
        """
        valid_meal_types = ['breakfast', 'lunch', 'dinner', 'brunch', 'other']

        if not meal_type or not meal_type.strip():
            raise ValidationError("Meal type cannot be empty")

        normalized = meal_type.strip().lower()
        if normalized not in valid_meal_types:
            raise ValidationError(
                f"Ivalid meal type. Must be one of {', '.join(valid_meal_types)}"
                )
            return self._visit_repo.filter_by_meal_type(normalized)

    def update_visit(
            self,
            visit_id: int,
            restaurant_id: int,
            visit_date: date,
            rating: int,
            meal_type: str,
            service_rating: Optional[int] = None,
            dishes_ordered: Optional[str] = None,
            recommended_dishes: Optional[str] = None,
            beverage_ordered: Optional[str] = None,
            total_cost: Optional[float] = None,
            notes: Optional[str] = None,
            would_return: bool = True
    ) -> Visit:
        """
        Update an existing Visit

        Business rules:
        - Visit must exist
        - Restaurant must exist
        - If changing restaurant_id, new restaurant cannot already have a visit
        - All validation is handled by the Visit model

        Args:
            visit_id: ID of visit to update
            restaurant_id: ID of the restaurant visited
            visit_date: Date of visit (first day of month)
            rating: Overall rating (1-5)
            meal_type: Type of meal
            service_rating: Service quality rating (optional)
            dishes_ordered: Dishes consumed (optional)
            recommended_dishes: Recommended items (optional)
            beverage_ordered: Beverages consumed (optional)
            total_cost: Total amount spent (optional)
            notes: Personal notes (optional)
            would_return: Whether would visit again

        Returns:
            Updated Visit object

        Raises:
            NotFoundError: If visit or restaurant doesn't exist
            BusinessRuleViolationError: If changing to restaurant that has a visit
            ValidationError: If any input is invalid
            RepositoryError: If database operation fails
        """
        # Verify visit exists
        existing_visit = self._visit_repo.get_by_id(visit_id)
        if existing_visit is None:
            raise NotFoundError(f"Visit with ID {visit_id} not found")

        # Verify restaurant exists
        restaurant = self._restaurant_repo.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError(f"Cannot update visit: Restaurant with ID {restaurant_id} not found")

        # If changing restaurant, check new restaurant doesn't have a visit
        if restaurant_id != existing_visit.restaurant_id:
            other_visit = self._visit_repo.get_by_restaurant_id(restaurant_id)
            if other_visit is not None:
                raise BusinessRuleViolationError(
                    f"Cannot move visit to restaurant '{restaurant.name}': "
                    f"that restaurant already has a visit recorded."
                )

        # Create updated Visit object (validation happens in __post_init__)
        updated_visit = Visit(
            id=visit_id,
            restaurant_id=restaurant_id,
            visit_date=visit_date,
            rating=rating,
            meal_type=meal_type,
            service_rating=service_rating,
            dishes_ordered=dishes_ordered,
            recommended_dishes=recommended_dishes,
            beverage_ordered=beverage_ordered,
            total_cost=total_cost,
            notes=notes,
            would_return=would_return
        )

        # Persist changes
        success = self._visit_repo.update(updated_visit)

        if not success:
            raise NotFoundError(f"Visit with ID {visit_id} not found")

        return updated_visit

    def delete_visit(self, visit_id: int) -> None:
        """
        Delete a visit by ID.
        Raises: NotFoundError: If visit doesn't exist
        RepositoryError: If database operation fails
        """
        # Verify visit exists
        visit = self._visit_repo.get_by_id(visit_id)
        if visit is None:
            raise NotFoundError(f"Visit with ID {visit_id} not found")

        # Delete the visit
        success = self._visit_repo.delete(visit_id)

        if not success:
            raise NotFoundError(f"Visit with ID {visit_id} not found")

    def delete_visit_for_restaurant(self, restaurant_id: int) -> None:
        """
        Delete the visit associated to a restaurant ID
        Raises: NotFoundError: If visit doesn't exist
        RepositoryError: If database operation fails
        """
        # Check if visit exists
        visit = self._visit_repo.get_by_restaurant_id(restaurant_id)
        if visit is None:
            raise NotFoundError(
                f"No visit found for restaurant with ID {restaurant_id}"
                )

        # Delete the visit
        success = self._visit_repo.delete_by_restaurant_id(restaurant_id)

        if not success:
            raise NotFoundError(
                f"No visit found for restaurant with ID {restaurant_id}"
            )
