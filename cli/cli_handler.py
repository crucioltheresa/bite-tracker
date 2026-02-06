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

    # ==================== RESTAURANT OPERATIONS ====================
    def add_restaurant(self):
        """Add a new restaurant."""
        self.print_header("Add New Restaurant")

        try:
            # Get required fields
            name = input("Restaurant name: ").strip()
            location = input("Location (city/address): ").strip()
            country = input("Country: ").strip()
            price_range = input("Price range (1=€, 2=€€, 3=€€€, 4=€€€€): ").strip()

            # Get optional fields
            cuisine_type = input("Cuisine type (optional, press Enter to skip): ").strip() or None
            phone = input("Phone (optional): ").strip() or None
            website = input("Website (optional): ").strip() or None
            social_media = input("Social media (optional): ").strip() or None

            # Create restaurant
            restaurant = self.restaurant_service.create_restaurant(
                name=name,
                location=location,
                country=country,
                price_range=int(price_range),
                cuisine_type=cuisine_type,
                phone=phone,
                website=website,
                social_media=social_media
            )

            self.print_success(f"Restaurant '{restaurant.name}' added successfully! (ID: {restaurant.id})")

        except ValidationError as e:
            self.print_error(str(e))
        except ValueError:
            self.print_error("Price range must be a number between 1 and 4")
        except Exception as e:
            self.print_error(f"Unexpected error: {e}")

    def view_all_restaurants(self):
        """View all restaurants."""
        self.print_header("All Restaurants")

        try:
            restaurants = self.restaurant_service.get_all_restaurants()

            if not restaurants:
                print("\nNo restaurants found. Add some first!")
                return

            print(f"\nTotal restaurants: {len(restaurants)}\n")
            for i, r in enumerate(restaurants, 1):
                print(f"{i}. {r}")
                if r.cuisine_type:
                    print(f"   Cuisine: {r.cuisine_type}")
                if r.phone:
                    print(f"   Phone: {r.phone}")
                print()

        except Exception as e:
            self.print_error(f"Failed to load restaurants: {e}")

    def search_restaurants(self):
        """Search restaurants by name."""
        self.print_header("Search Restaurants")

        try:
            search_term = input("Enter search term: ").strip()

            results = self.restaurant_service.search_restaurants(search_term)

            if not results:
                print(f"\nNo restaurants found matching '{search_term}'")
                return

            print(f"\nFound {len(results)} restaurant(s):\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r}")

        except ValidationError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Search failed: {e}")

    def filter_by_country(self):
        """Filter restaurants by country."""
        self.print_header("Filter by Country")

        try:
            country = input("Enter country name: ").strip()

            results = self.restaurant_service.get_restaurants_by_country(country)

            if not results:
                print(f"\nNo restaurants found in '{country}'")
                return

            print(f"\nRestaurants in {country} ({len(results)}):\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r}")

        except ValidationError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Filter failed: {e}")

    def delete_restaurant(self):
        """Delete a restaurant."""
        self.print_header("Delete Restaurant")

        try:
            # Show all restaurants first
            restaurants = self.restaurant_service.get_all_restaurants()
            if not restaurants:
                print("\nNo restaurants to delete.")
                return

            print("\nAvailable restaurants:")
            for i, r in enumerate(restaurants, 1):
                print(f"{i}. {r.name} (ID: {r.id})")

            restaurant_id = input("\nEnter restaurant ID to delete: ").strip()

            # Confirm deletion
            confirm = input(f"Are you sure you want to delete restaurant ID {restaurant_id}? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Deletion cancelled.")
                return

            self.restaurant_service.delete_restaurant(int(restaurant_id))
            self.print_success("Restaurant deleted successfully!")

        except NotFoundError as e:
            self.print_error(str(e))
        except BusinessRuleViolationError as e:
            self.print_error(str(e))
            print("\nTip: Delete the visit first, then delete the restaurant.")
        except ValueError:
            self.print_error("Restaurant ID must be a number")
        except Exception as e:
            self.print_error(f"Delete failed: {e}")
