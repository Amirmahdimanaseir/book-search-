"""
Refactored Book Database Management System with Production-Ready Features
A production-grade SQLite-based backend with logging, validation, and error handling.
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Tuple, Optional

from logger_config import setup_logger
from config import DATABASE_NAME, BOOK_TABLE_SCHEMA, DB_INDEXES
from validators import validate_book_data, validate_title, validate_author, validate_year, validate_isbn
from exceptions import (
    BookDatabaseError,
    BookNotFoundError,
    BookAlreadyExistsError,
    DatabaseError
)

logger = setup_logger(__name__)


@contextmanager
def get_connection():
    """
    Context manager for database connections.
    
    Ensures proper resource handling and auto-commit functionality.
    Automatically closes connection even if an exception occurs.
    
    Yields:
        sqlite3.Connection: Database connection object
        
    Example:
        with get_connection() as conn:
            conn.execute("SELECT * FROM book")
    """
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    try:
        yield conn
    except Exception as e:
        conn.rollback()
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        conn.close()


def initialize_database():
    """
    Initialize the database with proper schema and indexes.
    
    Creates the book table with constraints and sets up indexes for performance.
    Safe to call multiple times - uses CREATE TABLE IF NOT EXISTS.
    
    Raises:
        DatabaseError: If database initialization fails
    """
    try:
        with get_connection() as conn:
            # Create main table
            conn.execute(BOOK_TABLE_SCHEMA)
            logger.info("Book table created/verified")
            
            # Create indexes for performance
            for index_query in DB_INDEXES:
                conn.execute(index_query)
            logger.info("Database indexes created")
            
            conn.commit()
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise DatabaseError(f"Failed to initialize database: {e}")


def insert(title: str, author: str, year: int = None, isbn: str = "") -> bool:
    """
    Insert a new book record into the database.
    
    Validates all input data before insertion. Uses parameterized queries
    to prevent SQL injection. Handles duplicate ISBN gracefully.
    
    Args:
        title: Book title (required, 1-255 characters)
        author: Author name (required, 1-255 characters)
        year: Publication year (optional, 1000-2100)
        isbn: ISBN number (optional, 10-20 characters)
        
    Returns:
        bool: True if insertion successful, False otherwise
        
    Example:
        >>> insert("Python 101", "John Doe", 2020, "978-0134692011")
        True
    """
    try:
        # Validate input
        is_valid, message = validate_book_data(title, author, year, isbn)
        if not is_valid:
            logger.warning(f"Validation failed: {message}")
            return False
        
        # Normalize input
        title = title.strip()
        author = author.strip()
        isbn = isbn.strip() if isbn else ""
        
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO book (title, author, year, isbn) 
                   VALUES (?, ?, ?, ?)""",
                (title, author, year, isbn or None)
            )
            conn.commit()
        
        logger.info(f"Book inserted successfully: {title} by {author}")
        return True
        
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: book.isbn" in str(e):
            logger.warning(f"ISBN already exists: {isbn}")
            raise BookAlreadyExistsError(f"ISBN '{isbn}' already exists in database")
        logger.error(f"Integrity error: {e}")
        raise DatabaseError(f"Database integrity error: {e}")
        
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error during insertion: {e}")
        raise DatabaseError(f"Failed to insert book: {e}")
        
    except Exception as e:
        logger.error(f"Unexpected error during insertion: {e}")
        return False


def view(limit: int = 1000) -> List[Tuple]:
    """
    Retrieve all books from the database.
    
    Args:
        limit: Maximum number of records to retrieve (default: 1000)
        
    Returns:
        List of tuples containing (id, title, author, year, isbn, created_at)
        
    Example:
        >>> books = view()
        >>> for book in books:
        ...     print(book)
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, title, author, year, isbn, created_at 
                   FROM book ORDER BY created_at DESC LIMIT ?""",
                (limit,)
            )
            books = cursor.fetchall()
        logger.info(f"Retrieved {len(books)} books from database")
        return books
        
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error during view: {e}")
        raise DatabaseError(f"Failed to retrieve books: {e}")


def search(
    title: str = "",
    author: str = "",
    year: int = None,
    isbn: str = "",
    limit: int = 1000
) -> List[Tuple]:
    """
    Search for books by multiple criteria (AND logic).
    
    Supports partial matching for title and author (case-insensitive).
    All criteria are combined with AND logic.
    
    Args:
        title: Book title (partial match supported)
        author: Author name (partial match supported)
        year: Publication year (exact match)
        isbn: ISBN number (exact match)
        limit: Maximum results to return (default: 1000)
        
    Returns:
        List of matching book records
        
    Example:
        >>> results = search(title="Python", year=2020)
        >>> results = search(author="Smith")
    """
    try:
        query_parts = []
        params = []
        
        if title:
            validate_title(title)
            query_parts.append("title LIKE ?")
            params.append(f"%{title}%")
        
        if author:
            validate_author(author)
            query_parts.append("author LIKE ?")
            params.append(f"%{author}%")
        
        if year is not None:
            validate_year(year)
            query_parts.append("year = ?")
            params.append(year)
        
        if isbn:
            validate_isbn(isbn)
            query_parts.append("isbn = ?")
            params.append(isbn.strip())
        
        # If no criteria, return all books
        if not query_parts:
            logger.info("No search criteria provided, returning all books")
            return view(limit)
        
        where_clause = " AND ".join(query_parts)
        query = f"""SELECT id, title, author, year, isbn, created_at 
                    FROM book WHERE {where_clause} 
                    ORDER BY created_at DESC LIMIT ?"""
        params.append(limit)
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
        
        logger.info(f"Search found {len(results)} books matching criteria")
        return results
        
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise


def delete(book_id: int) -> bool:
    """
    Delete a book record by ID.
    
    Args:
        book_id: ID of the book to delete
        
    Returns:
        bool: True if deletion successful, False if book not found
        
    Raises:
        DatabaseError: If database operation fails
        
    Example:
        >>> delete(5)
        True
    """
    try:
        if not isinstance(book_id, int) or book_id <= 0:
            logger.warning(f"Invalid book_id: {book_id}")
            raise ValueError("book_id must be a positive integer")
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                logger.warning(f"Book not found for deletion: ID {book_id}")
                raise BookNotFoundError(f"Book with ID {book_id} not found")
            
            logger.info(f"Book deleted successfully: ID {book_id}")
            return True
            
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error during deletion: {e}")
        raise DatabaseError(f"Failed to delete book: {e}")


def update(
    book_id: int,
    title: str,
    author: str,
    year: int = None,
    isbn: str = ""
) -> bool:
    """
    Update an existing book record.
    
    Validates all input data before update. Updates only the provided fields.
    
    Args:
        book_id: ID of the book to update
        title: Updated book title
        author: Updated author name
        year: Updated publication year
        isbn: Updated ISBN number
        
    Returns:
        bool: True if update successful, False if book not found
        
    Raises:
        DatabaseError: If database operation fails
        
    Example:
        >>> update(5, "New Title", "New Author", 2021, "new-isbn")
        True
    """
    try:
        # Validate inputs
        is_valid, message = validate_book_data(title, author, year, isbn)
        if not is_valid:
            logger.warning(f"Validation failed: {message}")
            raise ValueError(message)
        
        if not isinstance(book_id, int) or book_id <= 0:
            logger.warning(f"Invalid book_id: {book_id}")
            raise ValueError("book_id must be a positive integer")
        
        # Normalize input
        title = title.strip()
        author = author.strip()
        isbn = isbn.strip() if isbn else ""
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE book 
                   SET title = ?, author = ?, year = ?, isbn = ?, updated_at = CURRENT_TIMESTAMP
                   WHERE id = ?""",
                (title, author, year, isbn or None, book_id)
            )
            conn.commit()
            
            if cursor.rowcount == 0:
                logger.warning(f"Book not found for update: ID {book_id}")
                raise BookNotFoundError(f"Book with ID {book_id} not found")
            
            logger.info(f"Book updated successfully: ID {book_id}")
            return True
            
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: book.isbn" in str(e):
            logger.warning(f"ISBN already exists: {isbn}")
            raise BookAlreadyExistsError(f"ISBN '{isbn}' already exists in database")
        logger.error(f"Integrity error: {e}")
        raise DatabaseError(f"Database integrity error: {e}")
        
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error during update: {e}")
        raise DatabaseError(f"Failed to update book: {e}")


def get_book_by_id(book_id: int) -> Optional[Tuple]:
    """
    Retrieve a specific book by ID.
    
    Args:
        book_id: ID of the book to retrieve
        
    Returns:
        Tuple containing (id, title, author, year, isbn, created_at) or None if not found
        
    Example:
        >>> book = get_book_by_id(5)
        >>> if book:
        ...     print(book[1])  # Print title
    """
    try:
        if not isinstance(book_id, int) or book_id <= 0:
            logger.warning(f"Invalid book_id: {book_id}")
            raise ValueError("book_id must be a positive integer")
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, title, author, year, isbn, created_at 
                   FROM book WHERE id = ?""",
                (book_id,)
            )
            book = cursor.fetchone()
        
        if not book:
            logger.debug(f"Book not found: ID {book_id}")
            return None
        
        logger.debug(f"Book retrieved: ID {book_id}")
        return book
        
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error during retrieval: {e}")
        raise DatabaseError(f"Failed to retrieve book: {e}")


def get_total_books() -> int:
    """
    Get total number of books in database.
    
    Returns:
        int: Total number of books
        
    Example:
        >>> total = get_total_books()
        >>> print(f"Total books: {total}")
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM book")
            count = cursor.fetchone()[0]
        
        logger.debug(f"Total books: {count}")
        return count
        
    except sqlite3.DatabaseError as e:
        logger.error(f"Database error during count: {e}")
        raise DatabaseError(f"Failed to count books: {e}")


# Initialize database on module import
try:
    initialize_database()
except Exception as e:
    logger.error(f"Failed to initialize database on import: {e}")
