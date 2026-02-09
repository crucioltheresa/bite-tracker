"""
Data import script for Bite Tracker.
Imports restaurant and visit data from a JSON file into the database.
Run once to populate initial data.
"""

import json
from datetime import datetime
from repositories import SqliteRestaurantRepository, SqliteVisitRepository
from services import RestaurantService, VisitService
from models import Restaurant, Visit


def parse_date(date_str):
    """Parse date string to date object."""
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def import_data(json_file="my_restaurants.json"):
    """
    Import restaurants and visits from JSON file.
    """
    print("\n" + "=" * 60)
    print("  BITE TRACKER - Data Import")
    print("=" * 60)

    # Initialize services
    print("\n  Initializing services...")
    restaurant_repo = SqliteRestaurantRepository()
    visit_repo = SqliteVisitRepository()
    restaurant_service = RestaurantService(restaurant_repo, visit_repo)
    visit_service = VisitService(visit_repo, restaurant_repo)
    print("  ✓ Services ready")

    # Load JSON data
    print(f"\n  Loading data from {json_file}...")
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"\n   ERROR: File '{json_file}' not found!")
        print("Please create the file in the project root directory.")
        return
    except json.JSONDecodeError as e:
        print(f"\n   ERROR: Invalid JSON format: {e}")
        return

    restaurants_data = data.get("restaurants", [])
    print(f"  ✓ Found {len(restaurants_data)} restaurant(s) to import")

    # Import each restaurant and its visit
    imported_count = 0
    skipped_count = 0
    error_count = 0

    print("\n  Importing data...\n")

    for idx, rest_data in enumerate(restaurants_data, 1):
        try:
            # Create restaurant
            restaurant = restaurant_service.create_restaurant(
                name=rest_data["name"],
                location=rest_data["location"],
                country=rest_data["country"],
                price_range=rest_data["price_range"],
                cuisine_type=rest_data.get("cuisine_type"),
                phone=rest_data.get("phone"),
                website=rest_data.get("website"),
                social_media=rest_data.get("social_media")
            )

            print(f"  [{idx}] ✓ Added: {restaurant.name}")

            # Create visit if present
            if "visit" in rest_data:
                visit_data = rest_data["visit"]

                visit = visit_service.create_visit(
                    restaurant_id=restaurant.id,
                    visit_date=parse_date(visit_data["visit_date"]),
                    rating=visit_data["rating"],
                    meal_type=visit_data["meal_type"],
                    service_rating=visit_data.get("service_rating"),
                    dishes_ordered=visit_data.get("dishes_ordered"),
                    recommended_dishes=visit_data.get("recommended_dishes"),
                    beverage_ordered=visit_data.get("beverage_ordered"),
                    total_cost=visit_data.get("total_cost"),
                    notes=visit_data.get("notes"),
                    would_return=visit_data.get("would_return", True)
                )

                print(f"      ✓ Added visit: {visit.get_formatted_date()}")

            imported_count += 1

        except KeyError as e:
            print(f"  [{idx}]  Missing required field: {e}")
            error_count += 1
        except Exception as e:
            print(f"  [{idx}]  Error importing {rest_data.get('name', 'Unknown')}: {e}")
            error_count += 1

    # Summary
    print("\n" + "=" * 60)
    print("  Import Complete!")
    print("=" * 60)
    print(f"\n  ✓ Successfully imported: {imported_count}")
    if skipped_count > 0:
        print(f"  ⊘ Skipped (already exists): {skipped_count}")
    if error_count > 0:
        print(f"   Errors: {error_count}")
    print("\n  You can now run 'python run.py' to see your data!\n")


if __name__ == "__main__":
    import_data()
