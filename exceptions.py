"""
Custom exceptions for the Book Database System
"""


class BookDatabaseError(Exception):
    """Base exception for Book Database System"""
    pass


class ValidationError(BookDatabaseError):
    """Raised when input validation fails"""
    pass


class TitleValidationError(ValidationError):
    """Raised when title validation fails"""
    pass


class AuthorValidationError(ValidationError):
    """Raised when author validation fails"""
    pass


class YearValidationError(ValidationError):
    """Raised when year validation fails"""
    pass


class ISBNValidationError(ValidationError):
    """Raised when ISBN validation fails"""
    pass


class BookNotFoundError(BookDatabaseError):
    """Raised when book is not found"""
    pass


class BookAlreadyExistsError(BookDatabaseError):
    """Raised when ISBN already exists"""
    pass


class DatabaseError(BookDatabaseError):
    """Raised when database operation fails"""
    pass
