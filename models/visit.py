"""
Visit domain model
Represents a visit to a restaurant with review details.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from exceptions import ValidationError


@dataclass
class Visit:
    """
    Represents a visit to a restaurant.

    Domain Rules:
    - Must be associated with a valid restaurant (restaurant_id required)
    - Visit date is stored as first day of month (stored as first day of month)
    - Overall rating must be 1-5 (required)
    - Service rating must be 1-5 if provided (optional)
    - Meal type must be valid option (breakfast/lunch/dinner/brunch/other)
    - Dishes, beverages, recommended dishes are optional text <= 500 chars
    - Total cost is optional, must be positive if provided
    - Notes are optional but if provided must be <= 1000 chars
    - Would return defaults to True

    Attributes:
        restaurant_id: ID of the restaurant visited (required)
        visit_date: Date of visit  (required)
        rating: Overall rating 1-5 stars (required)
        meal_type: Type of meal (required)
        id: Database ID (None for new visits, set by repository)
        service_rating: Service quality rating 1-5 (optional)
        dishes_ordered: Comma-separated list of dishes (optional)
        recommended_dishes: Comma-separated list of favourites (optional)
        beverage_ordered: Beverages consumed (optional)
        total_cost: Total amount spent (optional)
        notes: Personal notes about the visit (optional)
        would_return: Whether the user would visit again (optional)
    """

    # required fields
    restaurant_id: int
    visit_date: date
    rating: int
    meal_type: str

    # optional fields
    id: Optional[int] = None
    service_rating: Optional[int] = None
    dishes_ordered: Optional[str] = None
    recommended_dishes: Optional[str] = None
    beverage_ordered: Optional[str] = None
    total_cost: Optional[float] = None
    notes: Optional[str] = None
    would_return: bool = True

    def __post_init__(self):
        """Validate data immediately after object creation."""
        self._validate()

    def _validate(self):
        """
        Validates the visit data according to domain rules.
        Raises ValidationError if any validation rule is violated.
        """

        if not isinstance(self.restaurant_id, int) or self.resaurant_id <= 0:
            raise ValidationError("Valid restaurant ID is required.")

        if not isinstance(self.visit_date, date):
            raise ValidationError("Visit date must be a valid date.")
        if self.visit_date > date.today():
            raise ValidationError("Visit date cannot be in the future.")

        if not isinstance(self.rating, int):
            raise ValidationError("Rating must be an integer")
        if self.rating not in [1, 2, 3, 4, 5]:
            raise ValidationError("Rating must be between 1 and 5.")

        valid_meal_types = ['breakfast', 'lunch', 'dinner', 'brunch', 'other']
        if not self.meal_type or not isinstance(self.meal_type, str):
            raise ValidationError("Meal type is required.")
        if self.meal_type.lower() not in valid_meal_types:
            raise ValidationError(f"Meal type must be one of: {
                ', '.join(valid_meal_types)
                }.")

        if self.service_rating is not None:
            if not isinstance(self.service_rating, int):
                raise ValidationError("Service rating must be an integer.")
            if self.service_rating not in [1, 2, 3, 4, 5]:
                raise ValidationError("Service rating must be\
                                    between 1 and 5.")

        if self.dishes_ordered:
            if not isinstance(self.dishes_ordered, str):
                raise ValidationError("Dishes ordered must be a string.")
            if len(self.dishes_ordered) > 500:
                raise ValidationError("Dishes ordered must not\
                                    exceed 500 chars.")
            self.dishes_ordered = self.dishes_ordered.strip()

        if self.recommended_dishes:
            if not isinstance(self.recommended_dishes, str):
                raise ValidationError("Recommended dishes must be a string.")
            if len(self.recommended_dishes) > 500:
                raise ValidationError("Recommended dishes must not\
                                    exceed 500 chars.")
            self.recommended_dishes = self.recommended_dishes.strip()

        if self.beverage_ordered:
            if not isinstance(self.beverage_ordered, str):
                raise ValidationError("Beverage ordered must be a string.")
            if len(self.beverage_ordered) > 500:
                raise ValidationError("Beverage ordered must not\
                                    exceed 500 chars.")
            self.beverage_ordered = self.beverage_ordered.strip()

        if self.total_cost is not None:
            if not isinstance(self.total_cost, (int, float)):
                raise ValidationError("Total cost must be a number.")
            if self.total_cost < 0:
                raise ValidationError("Total cost cannot be negative.")

        if self.notes is not None:
            if not isinstance(self.notes, str):
                raise ValidationError("Notes must be a string.")
            if len(self.notes) > 1000:
                raise ValidationError("Notes must not exceed 1000 chars.")
            self.notes = self.notes.strip()

        if not isinstance(self.would_return, bool):
            raise ValidationError("Would return must be True or False.")

        # Normalize meals_type to lowercase for consistency
        self.meal_type = self.meal_type.lower().strip()
