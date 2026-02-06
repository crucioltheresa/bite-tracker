"""
Bite Tracker - Restaurant Visit & Review Manager
A CLI application for tracking restaurant visits and reviews.
"""

from repositories import SqliteRestaurantRepository, SqliteVisitRepository
from services import RestaurantService, VisitService
from cli import CLIHandler, MainMenu


def main():
    """
    Main entry point for Bite Tracker application.
    Initializes all layers (repositories, services, CLI) with
    dependency injection and starts the main menu loop.
    """

    # Display welcome banner
    print("\n" + "=" * 60)
    print("  BITE TRACKER")
    print("  Restaurant Visit & Review Manager")
    print("=" * 60)
    print("\n  Initializing application...")

    # Initialize repository layer (data access)
    try:
        restaurant_repo = SqliteRestaurantRepository()
        visit_repo = SqliteVisitRepository()
        print("  ✓ Database initialized")
    except Exception as e:
        print(f"\n   ERROR: Failed to initialize database: {e}")
        print("  Please check that the 'data' directory is writable.\n")
        return

    # Initialize service layer (business logic)
    try:
        restaurant_service = RestaurantService(restaurant_repo, visit_repo)
        visit_service = VisitService(visit_repo, restaurant_repo)
        print("  ✓ Services initialized")
    except Exception as e:
        print(f"\n   ERROR: Failed to initialize services: {e}\n")
        return

    # Initialize CLI layer (user interface)
    try:
        cli_handler = CLIHandler(restaurant_service, visit_service)
        main_menu = MainMenu(cli_handler)
        print("  ✓ User interface ready")
    except Exception as e:
        print(f"\n   ERROR: Failed to initialize CLI: {e}\n")
        return

    print("\n  Starting application...\n")

    # Run the application
    try:
        main_menu.run()
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\n\n" + "=" * 60)
        print("  Application interrupted by user.")
        print("  Thank you for using Bite Tracker!")
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n\n UNEXPECTED ERROR: {e}")
        print("Please report this issue.\n")


if __name__ == "__main__":
    main()
