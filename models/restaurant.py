"""
Restaurant domain model.
Defines the Restaurant class with built-in validation.
Enforces data integrity and domain rules.
"""


from dataclasses import dataclass
from typing import Optional
from exceptions import ValidationError


@dataclass
class Restaurant:
    """
    Represents a restaurant entity.

    Domain Rules:
    - Name must be a non-empty string and <= 100 characters
    - Location must be a non-empty string and <= 150 characters
    - Country must be non-empty and <= 100 characters
    - Price Range must be 1-4 (representing €, €€, €€€, €€€€)
    - Cuisine Type is optional but if provided must be <= 50 characters
    - Phone is optional but if provided must be <= 20 characters
    - Website is optional but if provided must be <= 200 characters
    - Social media URL is optional but if provided must be <= 50 characters


    Attributes:
    name: Restaurant name (required)
    location: Address/City (required)
    country: Country where restaurant is located (required)
    price_range: Price category 1-4 (required)
    id: Database ID (none for new restaurants)
    cuisine_type: Type of cuisine (optional)
    phone: Contact phone number (optional)
    website: Restaurant website URL (optional)
    social_media: Social media profile URL (optional)
    """

    # required fields
    name: str
    location: str
    country: str
    price_range: int

    # optional fields
    id: Optional[int] = None
    cuisine_type: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    social_media: Optional[str] = None

    def __post_init__(self):
        """Validate data immediately after object creation."""
        self._validate()

    def _validate(self):
        """
        Validate all fields according to domain rules.
        Raises ValidationError if any validation rule is violated".
        """

        if not self.name or not self.name.strip():
            raise ValidationError("Restaurant name is required.")
        if len(self.name) > 100:
            raise ValidationError("Restaurant name must not exceed 100 chars.")

        if not self.location or not self.location.strip():
            raise ValidationError("Location is required.")
        if len(self.location) > 150:
            raise ValidationError("Location must not exceed 150 chars.")

        if not self.country or not self.country.strip():
            raise ValidationError("Country is required.")
        if len(self.country) > 100:
            raise ValidationError("Country must not exceed 100 chars.")

        if not isinstance(self.price_range, int):
            raise ValidationError("Price range must be an integer.")
        if self.price_range not in [1, 2, 3, 4]:
            raise ValidationError("Price range must be between 1 and 4.")

        if self.cuisine_type and len(self.cuisine_type) > 50:
            raise ValidationError("Cuisine type must not exceed 50 chars.")
        if self.phone and len(self.phone) > 20:
            raise ValidationError("Phone number must not exceed 20 chars.")
        if self.website and len(self.website) > 200:
            raise ValidationError("Website URL must not exceed 200 chars.")
        if self.social_media and len(self.social_media) > 200:
            raise ValidationError("Social media URL must not exceed 50 chars.")

        # Strip whitespace from string fields
        self.name = self.name.strip()
        self.location = self.location.strip()
        self.country = self.country.strip()
        if self.cuisine_type:
            self.cuisine_type = self.cuisine_type.strip()
        if self.phone:
            self.phone = self.phone.strip()
        if self.website:
            self.website = self.website.strip()
        if self.social_media:
            self.social_media = self.social_media.strip()

    def get_price_symbol(self) -> str:
        """Returns a string os euro symbols (€, €€, etc.)
        based on price_range."""
        return '€' * self.price_range

    def __str__(self) -> str:
        """String representation for display purposes."""
        cuisine = f" ({self.cuisine_type})" if self.cuisine_type else ""
        return f"{self.name}{cuisine} - {self.location},\
            {self.country} - {self.get_price_symbol()}"
