"""
Input validation utilities for CLI user input.
Handles validation and sanitization of user input
from the command line, separate from domain model validation.
"""

from datetime import datetime, date
from typing import Optional
from exceptions import ValidationError


class InputValidator:
    """
    Responsible for converting raw user input
    into validated data that can be used to create domain models.
    """

    @staticmethod
    def validate_non_empty_string(value: str, field_name: str, max_length: Optional[int] = None) -> str:
        """
        Validate that a string is non-empty.
        Raises: ValidationError: If validation fails
        """
        if not value or not value.strip():
            raise ValidationError(f"{field_name} cannot be empty")

        stripped = value.strip()

        if max_length and len(stripped) > max_length:
            raise ValidationError(
                f"{field_name} must not exceed {max_length} characters"
            )

        return stripped

    @staticmethod
    def validate_date(value: str) -> date:
        """
        Validate and convert date input.
        Raises: ValidationError: If input is not a valid date or is in the future
        """
        formats = [
            "%Y-%m-%d",      # 2024-03-15
            "%d/%m/%Y",      # 15/03/2024
            "%d-%m-%Y"       # 15-03-2024
        ]

        for date_format in formats:
            try:
                parsed_date = datetime.strptime(value.strip(), date_format).date()

                # Check if date is in the future
                if parsed_date > date.today():
                    raise ValidationError("Visit date cannot be in the future")

                return parsed_date
            except ValueError:
                continue

        # If no format worked
        raise ValidationError(
            "Invalid date format. Use YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY"
        )
