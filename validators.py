"""
Input validation module for the Book Database System
"""

from typing import Tuple
from config import BOOK_CONSTRAINTS
from exceptions import (
    TitleValidationError,
    AuthorValidationError,
    YearValidationError,
    ISBNValidationError
)


def validate_title(title: str) -> Tuple[bool, str]:
    """
    Validate book title.
    
    Args:
        title: Book title to validate
        
    Returns:
        Tuple of (is_valid, message)
        
    Raises:
        TitleValidationError: If validation fails
    """
    constraints = BOOK_CONSTRAINTS["title"]
    
    if not title:
        raise TitleValidationError("Title cannot be empty")
    
    title_stripped = title.strip()
    if not title_stripped:
        raise TitleValidationError("Title cannot contain only whitespace")
    
    if len(title_stripped) < constraints["min_length"]:
        raise TitleValidationError(
            f"Title must be at least {constraints['min_length']} character(s)"
        )
    
    if len(title_stripped) > constraints["max_length"]:
        raise TitleValidationError(
            f"Title must not exceed {constraints['max_length']} characters"
        )
    
    return True, "Title is valid"


def validate_author(author: str) -> Tuple[bool, str]:
    """
    Validate author name.
    
    Args:
        author: Author name to validate
        
    Returns:
        Tuple of (is_valid, message)
        
    Raises:
        AuthorValidationError: If validation fails
    """
    constraints = BOOK_CONSTRAINTS["author"]
    
    if not author:
        raise AuthorValidationError("Author cannot be empty")
    
    author_stripped = author.strip()
    if not author_stripped:
        raise AuthorValidationError("Author cannot contain only whitespace")
    
    if len(author_stripped) < constraints["min_length"]:
        raise AuthorValidationError(
            f"Author must be at least {constraints['min_length']} character(s)"
        )
    
    if len(author_stripped) > constraints["max_length"]:
        raise AuthorValidationError(
            f"Author must not exceed {constraints['max_length']} characters"
        )
    
    return True, "Author is valid"


def validate_year(year: int) -> Tuple[bool, str]:
    """
    Validate publication year.
    
    Args:
        year: Publication year to validate
        
    Returns:
        Tuple of (is_valid, message)
        
    Raises:
        YearValidationError: If validation fails
    """
    if year is None:
        return True, "Year is optional and valid"
    
    constraints = BOOK_CONSTRAINTS["year"]
    
    if not isinstance(year, int):
        raise YearValidationError(f"Year must be an integer, got {type(year).__name__}")
    
    if year < constraints["min_value"] or year > constraints["max_value"]:
        raise YearValidationError(
            f"Year must be between {constraints['min_value']} and {constraints['max_value']}, got {year}"
        )
    
    return True, "Year is valid"


def validate_isbn(isbn: str) -> Tuple[bool, str]:
    """
    Validate ISBN.
    
    Args:
        isbn: ISBN to validate
        
    Returns:
        Tuple of (is_valid, message)
        
    Raises:
        ISBNValidationError: If validation fails
    """
    if not isbn:
        return True, "ISBN is optional and valid"
    
    constraints = BOOK_CONSTRAINTS["isbn"]
    
    isbn_cleaned = isbn.replace("-", "").replace(" ", "")
    
    if len(isbn_cleaned) < constraints["min_length"]:
        raise ISBNValidationError(
            f"ISBN must be at least {constraints['min_length']} characters"
        )
    
    if len(isbn_cleaned) > constraints["max_length"]:
        raise ISBNValidationError(
            f"ISBN must not exceed {constraints['max_length']} characters"
        )
    
    # Check if ISBN contains only digits and hyphens
    if not all(c.isdigit() or c == '-' or c == ' ' for c in isbn):
        raise ISBNValidationError("ISBN can only contain digits, hyphens, and spaces")
    
    return True, "ISBN is valid"


def validate_book_data(
    title: str,
    author: str,
    year: int = None,
    isbn: str = ""
) -> Tuple[bool, str]:
    """
    Validate all book data at once.
    
    Args:
        title: Book title
        author: Author name
        year: Publication year (optional)
        isbn: ISBN (optional)
        
    Returns:
        Tuple of (is_valid, message)
    """
    try:
        validate_title(title)
        validate_author(author)
        validate_year(year)
        validate_isbn(isbn)
        return True, "All book data is valid"
    except Exception as e:
        return False, str(e)
