"""
Unit tests for book database backend.
Run with: pytest test_backend.py -v
"""

import pytest
import os
import sqlite3
from backend import (
    insert, view, search, update, delete, 
    get_book_by_id, get_total_books, initialize_database,
    DATABASE_NAME
)


@pytest.fixture
def setup_teardown():
    """Setup and teardown for each test."""
    # Setup: Create fresh database
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    initialize_database()
    
    yield
    
    # Teardown: Clean up
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)


def test_insert_book(setup_teardown):
    """Test inserting a book."""
    result = insert(
        title="Python Basics",
        author="John Doe",
        year=2020,
        isbn="123-456"
    )
    assert result is True
    assert get_total_books() == 1


def test_insert_duplicate_isbn(setup_teardown):
    """Test that duplicate ISBN fails."""
    insert("Book 1", "Author 1", 2020, "123-456")
    result = insert("Book 2", "Author 2", 2021, "123-456")
    assert result is False


def test_view_all_books(setup_teardown):
    """Test viewing all books."""
    insert("Book 1", "Author 1", 2020, "111")
    insert("Book 2", "Author 2", 2021, "222")
    
    books = view()
    assert len(books) == 2
    assert books[0][1] == "Book 1"
    assert books[1][1] == "Book 2"


def test_search_by_title(setup_teardown):
    """Test searching by title."""
    insert("Python Programming", "Guido", 2020, "111")
    insert("Java Basics", "James", 2021, "222")
    
    results = search(title="Python")
    assert len(results) == 1
    assert results[0][1] == "Python Programming"


def test_search_by_author(setup_teardown):
    """Test searching by author."""
    insert("Book 1", "John Smith", 2020, "111")
    insert("Book 2", "Jane Doe", 2021, "222")
    
    results = search(author="John")
    assert len(results) == 1
    assert results[0][2] == "John Smith"


def test_search_by_year(setup_teardown):
    """Test searching by year."""
    insert("Book 1", "Author 1", 2020, "111")
    insert("Book 2", "Author 2", 2021, "222")
    insert("Book 3", "Author 3", 2020, "333")
    
    results = search(year=2020)
    assert len(results) == 2


def test_search_multiple_criteria(setup_teardown):
    """Test searching with multiple criteria (AND logic)."""
    insert("Python Programming", "Guido", 2020, "111")
    insert("Python Basics", "John", 2021, "222")
    
    results = search(title="Python", year=2020)
    assert len(results) == 1
    assert results[0][1] == "Python Programming"


def test_get_book_by_id(setup_teardown):
    """Test getting a book by ID."""
    insert("Book 1", "Author 1", 2020, "111")
    
    book = get_book_by_id(1)
    assert book is not None
    assert book[1] == "Book 1"
    assert book[2] == "Author 1"


def test_get_nonexistent_book(setup_teardown):
    """Test getting a non-existent book."""
    book = get_book_by_id(999)
    assert book is None


def test_update_book(setup_teardown):
    """Test updating a book."""
    insert("Old Title", "Old Author", 2020, "111")
    
    result = update(
        book_id=1,
        title="New Title",
        author="New Author",
        year=2021,
        isbn="222"
    )
    assert result is True
    
    updated_book = get_book_by_id(1)
    assert updated_book[1] == "New Title"
    assert updated_book[2] == "New Author"
    assert updated_book[4] == "222"


def test_update_nonexistent_book(setup_teardown):
    """Test updating a non-existent book."""
    result = update(999, "Title", "Author", 2020, "111")
    assert result is False


def test_delete_book(setup_teardown):
    """Test deleting a book."""
    insert("Book 1", "Author 1", 2020, "111")
    assert get_total_books() == 1
    
    result = delete(1)
    assert result is True
    assert get_total_books() == 0


def test_delete_nonexistent_book(setup_teardown):
    """Test deleting a non-existent book."""
    result = delete(999)
    assert result is False


def test_get_total_books(setup_teardown):
    """Test getting total book count."""
    assert get_total_books() == 0
    
    insert("Book 1", "Author 1", 2020, "111")
    assert get_total_books() == 1
    
    insert("Book 2", "Author 2", 2021, "222")
    assert get_total_books() == 2
    
    delete(1)
    assert get_total_books() == 1


def test_empty_search_returns_all(setup_teardown):
    """Test that empty search returns all books."""
    insert("Book 1", "Author 1", 2020, "111")
    insert("Book 2", "Author 2", 2021, "222")
    
    results = search()
    assert len(results) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
