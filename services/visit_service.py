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
