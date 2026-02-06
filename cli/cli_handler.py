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

# ==================== VISIT OPERATIONS ====================
    def add_visit(self):
        """Add a new visit to a restaurant."""
        self.print_header("Add New Visit")

        try:
            # First, show available restaurants
            restaurants = self.restaurant_service.get_all_restaurants()
            if not restaurants:
                print("\nNo restaurants available. Add a restaurant first!")
                return

            print("\nAvailable restaurants:")
            for i, r in enumerate(restaurants, 1):
                # Check if restaurant already has a visit
                existing_visit = self.visit_service.get_visit_for_restaurant(r.id)
                status = " [HAS VISIT]" if existing_visit else ""
                print(f"{i}. {r.name} (ID: {r.id}){status}")

            # Get restaurant ID
            restaurant_id = input("\nEnter restaurant ID: ").strip()

            # Get visit details
            print("\nVisit Details:")
            visit_date_str = input("Visit date (YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY): ").strip()
            rating = input("Overall rating (1-5): ").strip()
            meal_type = input("Meal type (breakfast/lunch/dinner/brunch/other): ").strip()

            # Optional fields
            print("\nOptional Details (press Enter to skip):")
            service_rating = input("Service rating (1-5): ").strip() or None
            dishes_ordered = input("Dishes ordered: ").strip() or None
            recommended_dishes = input("Recommended dishes: ").strip() or None
            beverage_ordered = input("Beverages: ").strip() or None
            total_cost = input("Total cost (€): ").strip() or None
            notes = input("Notes: ").strip() or None
            would_return = input("Would you return? (yes/no, default yes): ").strip().lower() or "yes"

            # Parse date
            visit_date = self.validator.validate_date(visit_date_str)

            # Parse optional numeric fields
            service_rating_int = int(service_rating) if service_rating else None
            total_cost_float = float(total_cost) if total_cost else None

            # Parse boolean
            would_return_bool = would_return in ['yes', 'y']

            # Create visit
            visit = self.visit_service.create_visit(
                restaurant_id=int(restaurant_id),
                visit_date=visit_date,
                rating=int(rating),
                meal_type=meal_type,
                service_rating=service_rating_int,
                dishes_ordered=dishes_ordered,
                recommended_dishes=recommended_dishes,
                beverage_ordered=beverage_ordered,
                total_cost=total_cost_float,
                notes=notes,
                would_return=would_return_bool
            )

            self.print_success(f"Visit added successfully! (ID: {visit.id})")

        except NotFoundError as e:
            self.print_error(str(e))
        except BusinessRuleViolationError as e:
            self.print_error(str(e))
            print("\nThis restaurant already has a visit. Update it instead.")
        except ValidationError as e:
            self.print_error(str(e))
        except ValueError as e:
            self.print_error(f"Invalid number format: {e}")
        except Exception as e:
            self.print_error(f"Failed to add visit: {e}")

    def view_all_visits(self):
        """View all visits with restaurant details."""
        self.print_header("All Visits")

        try:
            visits = self.visit_service.get_all_visits()

            if not visits:
                print("\nNo visits recorded yet. Add some first!")
                return

            print(f"\nTotal visits: {len(visits)}\n")
            for i, v in enumerate(visits, 1):
                # Get the restaurant for this visit
                restaurant = self.restaurant_service.get_restaurant(v.restaurant_id)

                print(f"{i}. {restaurant.name}")
                print(f"   {v}")
                if v.service_rating:
                    print(f"   Service: {v.get_service_rating_stars()}")
                if v.dishes_ordered:
                    print(f"   Dishes: {v.dishes_ordered}")
                if v.total_cost:
                    print(f"   Cost: {v.get_formatted_cost()}")
                if v.notes:
                    print(f"   Notes: {v.notes}")
                print()

        except Exception as e:
            self.print_error(f"Failed to load visits: {e}")

    def filter_visits_by_rating(self):
        """Filter visits by minimum rating."""
        self.print_header("Filter Visits by Rating")

        try:
            min_rating = input("Minimum rating (1-5): ").strip()

            visits = self.visit_service.get_top_rated_visits(int(min_rating))

            if not visits:
                print(f"\nNo visits found with rating >= {min_rating}")
                return

            print(f"\nVisits with rating >= {min_rating} ({len(visits)}):\n")
            for i, v in enumerate(visits, 1):
                restaurant = self.restaurant_service.get_restaurant(v.restaurant_id)
                print(f"{i}. {restaurant.name} - {v.get_formatted_date()} - {v.get_rating_stars()}")

        except ValidationError as e:
            self.print_error(str(e))
        except ValueError:
            self.print_error("Rating must be a number between 1 and 5")
        except Exception as e:
            self.print_error(f"Filter failed: {e}")

    def filter_visits_by_meal_type(self):
        """Filter visits by meal type."""
        self.print_header("Filter Visits by Meal Type")

        try:
            print("\nMeal types: breakfast, lunch, dinner, brunch, other")
            meal_type = input("Enter meal type: ").strip()

            visits = self.visit_service.get_visits_by_meal_type(meal_type)

            if not visits:
                print(f"\nNo {meal_type} visits found")
                return

            print(f"\n{meal_type.capitalize()} visits ({len(visits)}):\n")
            for i, v in enumerate(visits, 1):
                restaurant = self.restaurant_service.get_restaurant(v.restaurant_id)
                print(f"{i}. {restaurant.name} - {v.get_formatted_date()}")

        except ValidationError as e:
            self.print_error(str(e))
        except Exception as e:
            self.print_error(f"Filter failed: {e}")

    def delete_visit(self):
        """Delete a visit."""
        self.print_header("Delete Visit")

        try:
            # Show all visits first
            visits = self.visit_service.get_all_visits()
            if not visits:
                print("\nNo visits to delete.")
                return

            print("\nAvailable visits:")
            for i, v in enumerate(visits, 1):
                restaurant = self.restaurant_service.get_restaurant(v.restaurant_id)
                print(f"{i}. {restaurant.name} - {v.get_formatted_date()} (ID: {v.id})")

            visit_id = input("\nEnter visit ID to delete: ").strip()

            # Confirm deletion
            confirm = input(f"Are you sure you want to delete visit ID {visit_id}? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Deletion cancelled.")
                return

            self.visit_service.delete_visit(int(visit_id))
            self.print_success("Visit deleted successfully!")

        except NotFoundError as e:
            self.print_error(str(e))
        except ValueError:
            self.print_error("Visit ID must be a number")
        except Exception as e:
            self.print_error(f"Delete failed: {e}")
