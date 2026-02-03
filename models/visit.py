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
