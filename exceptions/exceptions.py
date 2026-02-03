"""
Custom exception classes for handling
specific error scenarios in the application.
"""


class BiteTrackerError(Exception):
    """Base exception for all Bite Tracker errors."""
    pass


class ValidationError(BiteTrackerError):
    """Raised when input validation fails."""
    pass


class RepositoryError(BiteTrackerError):
    """Raised when database operations fail."""
    pass


class NotFoundError(RepositoryError):
    """Raised when a requested entity is not found in the database."""
    pass


class BusinessRuleViolationError(BiteTrackerError):
    """Raised when business rule is violated."""
    pass
