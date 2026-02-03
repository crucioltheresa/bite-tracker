"""Restaurant domain model.
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
    - Price Range must be 1-4 (representing €, €€, €€€, €€€€)
    - Cuisine Type is optional but if provided must be <= 50 characters
    - Phone is optional but if provided must be <= 20 characters
    - Website is optional but if provided must be <= 200 characters


    Attributes:
    name: Restaurant name (required)
    location: Physical address or area (required)
    price_range: Price category 1-4 (required)
    id: Database ID (none for new restaurants)
    cuisine_type: Type of cuisine (optional)
    phone: Contact phone number (optional)
    website: Restaurant website URL (optional)
    """

    # required fields
    name: str
    location: str
    price_range: int

    # optional fields
    id: Optional[int] = None
    cuisine_type: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
