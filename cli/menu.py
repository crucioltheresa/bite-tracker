"""
Main menu system for Bite Tracker.
Handles navigation and user flow through the application.
"""

from cli.cli_handler import CLIHandler


class MainMenu:
    """Main menu for Bite Tracker application."""
    def __init__(self, cli_handler: CLIHandler):
        """Initialize with CLI handler dependency."""
        self.cli = cli_handler
        self.running = True
        self.data_modified = False

    def display_main_menu(self):
        """Display the main menu options."""
        print("\n" + "=" * 60)
        print("  BITE TRACKER - Restaurant Visit Manager")
        print("=" * 60)
        print("\n[RESTAURANTS]")
        print("  1. Add Restaurant")
        print("  2. View All Restaurants")
        print("  3. Search Restaurants")
        print("  4. Filter by Country")
        print("  5. Delete Restaurant")
        print("\n[VISITS]")
        print("  6. Add Visit")
        print("  7. View All Visits")
        print("  8. Filter Visits by Rating")
        print("  9. Filter Visits by Meal Type")
        print("  10. Delete Visit")
        print("\n[OTHER]")
        print("  0. Exit")
        print("=" * 60)

    def run(self):
        """Run the main menu loop."""
        while self.running:
            self.display_main_menu()
            choice = input("\nEnter your choice: ").strip()

            self.handle_choice(choice)

    def handle_choice(self, choice: str):
        """Handle user menu selection."""
        # Restaurant operations
        if choice == '1':
            self.cli.add_restaurant()
            self.data_modified = True
            self.cli.pause()
        elif choice == '2':
            self.cli.view_all_restaurants()
            self.cli.pause()
        elif choice == '3':
            self.cli.search_restaurants()
            self.cli.pause()
        elif choice == '4':
            self.cli.filter_by_country()
            self.cli.pause()
        elif choice == '5':
            self.cli.delete_restaurant()
            self.data_modified = True
            self.cli.pause()

        # Visit operations
        elif choice == '6':
            self.cli.add_visit()
            self.data_modified = True
            self.cli.pause()
        elif choice == '7':
            self.cli.view_all_visits()
            self.cli.pause()
        elif choice == '8':
            self.cli.filter_visits_by_rating()
            self.cli.pause()
        elif choice == '9':
            self.cli.filter_visits_by_meal_type()
            self.cli.pause()
        elif choice == '10':
            self.cli.delete_visit()
            self.data_modified = True
            self.cli.pause()

        # Exit
        elif choice == '0':
            self.exit_application()

        # Invalid choice
        else:
            print("\n Invalid choice. Please enter a number from the menu.")
            self.cli.pause()

    def exit_application(self):
        """Exit the application gracefully."""
        print("\n" + "=" * 60)
        print("  Thank you for using Bite Tracker!")
        if self.data_modified:
            print("  Your restaurant visits have been saved.")
        print("=" * 60 + "\n")
        self.running = False
