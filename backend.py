"""
Book Database Management System
A simple SQLite-based backend for managing book information.
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Tuple, Optional


DATABASE_NAME = "books.db"


@contextmanager
def get_connection():
    """
    Context manager for database connections.
    Ensures proper resource handling and auto-commit functionality.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    try:
        yield conn
    finally:
        conn.close()


def initialize_database():
    """Initialize the database with proper schema."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS book (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER,
                isbn TEXT UNIQUE
            )
        """)
        conn.commit()


def insert(title: str, author: str, year: int, isbn: str) -> bool:
    """
    Insert a new book record into the database.
    
    Args:
        title: Book title
        author: Author name
        year: Publication year
        isbn: ISBN number
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO book (title, author, year, isbn) VALUES (?, ?, ?, ?)",
                (title, author, year, isbn)
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return False


def view() -> List[Tuple]:
    """
    Retrieve all books from the database.
    
    Returns:
        List of tuples containing book information
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, year, isbn FROM book")
        return cursor.fetchall()


def search(title: str = "", author: str = "", year: Optional[int] = None, 
           isbn: str = "") -> List[Tuple]:
    """
    Search for books by title, author, year, or ISBN.
    
    Args:
        title: Book title (partial match supported)
        author: Author name (partial match supported)
        year: Publication year
        isbn: ISBN number
        
    Returns:
        List of matching book records
    """
    query_parts = []
    params = []
    
    if title:
        query_parts.append("title LIKE ?")
        params.append(f"%{title}%")
    
    if author:
        query_parts.append("author LIKE ?")
        params.append(f"%{author}%")
    
    if year:
        query_parts.append("year = ?")
        params.append(year)
    
    if isbn:
        query_parts.append("isbn = ?")
        params.append(isbn)
    
    if not query_parts:
        return view()
    
    query = "SELECT id, title, author, year, isbn FROM book WHERE " + " AND ".join(query_parts)
    
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()


def delete(book_id: int) -> bool:
    """
    Delete a book record by ID.
    
    Args:
        book_id: ID of the book to delete
        
    Returns:
        bool: True if deletion successful, False otherwise
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM book WHERE id = ?", (book_id,))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Error deleting book: {e}")
        return False


def update(book_id: int, title: str, author: str, year: int, isbn: str) -> bool:
    """
    Update an existing book record.
    
    Args:
        book_id: ID of the book to update
        title: Updated book title
        author: Updated author name
        year: Updated publication year
        isbn: Updated ISBN number
        
    Returns:
        bool: True if update successful, False otherwise
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE book SET title = ?, author = ?, year = ?, isbn = ? WHERE id = ?",
                (title, author, year, isbn, book_id)
            )
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.IntegrityError as e:
        print(f"Error: {e}")
        return False
    except Exception as e:
        print(f"Error updating book: {e}")
        return False


def get_book_by_id(book_id: int) -> Optional[Tuple]:
    """
    Retrieve a specific book by ID.
    
    Args:
        book_id: ID of the book
        
    Returns:
        Tuple containing book information or None if not found
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author, year, isbn FROM book WHERE id = ?", (book_id,))
        return cursor.fetchone()


def get_total_books() -> int:
    """Get total number of books in database."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM book")
        return cursor.fetchone()[0]


# Initialize database on import
initialize_database()
