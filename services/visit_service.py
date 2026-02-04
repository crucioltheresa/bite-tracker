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
