"""
Custom exceptions used across the project.
"""

class ApplicationError(Exception):
    """Base exception for the application."""
    pass

class ValidationError(ApplicationError):
    """Raised when validation fails."""
    pass

class DatabaseError(ApplicationError):
    """Raised for database-related errors."""
    pass