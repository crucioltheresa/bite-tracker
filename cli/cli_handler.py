"""
CLI Handler for Bite Tracker.
Handles all user interaction for restaurants and visits.
"""

from datetime import date, datetime
from typing import Optional
from services import RestaurantService, VisitService
from exceptions import (
    ValidationError,
    NotFoundError,
    BusinessRuleViolationError,
    RepositoryError
)
from validators import InputValidator


class CLIHandler:
    """Handles all CLI interactions."""

    def __init__(self, restaurant_service: RestaurantService, visit_service: VisitService):
        """Initialize with service dependencies."""
        self.restaurant_service = restaurant_service
        self.visit_service = visit_service
        self.validator = InputValidator()

    def clear_screen(self):
        """Clear the terminal screen."""
        print("\n" * 2)  # Simple spacing instead of actual clear

    def print_header(self, title: str):
        """Print a formatted header."""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def print_error(self, message: str):
        """Print an error message."""
        print(f"\n ERROR: {message}")

    def print_success(self, message: str):
        """Print a success message."""
        print(f"\n {message}")

    def pause(self):
        """Wait for user to press Enter."""
        input("\nPress Enter to continue...")
