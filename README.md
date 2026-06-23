# Book Search Database System

A simple yet professional SQLite-based book management system with CRUD operations.

## 📋 Overview

This project provides a backend database system for managing book information. It supports creating, reading, updating, and deleting book records with proper error handling and validation.

## ✨ Features

- ✅ Create, Read, Update, Delete (CRUD) operations
- ✅ Search books by title, author, year, or ISBN
- ✅ Proper database connection management using context managers
- ✅ Type hints and comprehensive docstrings
- ✅ Error handling and validation
- ✅ SQLite database with automatic initialization
- ✅ Support for partial search queries

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/Amirmahdimanaseir/book-search-.git
cd book-search-

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 📚 Usage

### Basic Operations

```python
from backend import insert, view, search, update, delete, get_book_by_id

# Add a new book
insert(
    title="Python Programming",
    author="Guido van Rossum",
    year=2020,
    isbn="123-456-789"
)

# View all books
all_books = view()
print(all_books)

# Search for books
results = search(title="Python")
results = search(author="Guido")
results = search(year=2020)

# Get a specific book
book = get_book_by_id(1)

# Update a book
update(
    book_id=1,
    title="Advanced Python",
    author="Guido van Rossum",
    year=2021,
    isbn="123-456-790"
)

# Delete a book
delete(book_id=1)
```

## 🗂️ Project Structure

```
book-search-/
├── backend.py           # Main database module
├── requirements.txt     # Project dependencies
├── README.md           # This file
└── books.db            # SQLite database (auto-created)
```

## 🔧 Database Schema

```sql
CREATE TABLE book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    year INTEGER,
    isbn TEXT UNIQUE
)
```

## 📋 API Reference

### `initialize_database()`
Initialize the database with proper schema.

### `insert(title, author, year, isbn) -> bool`
Insert a new book record.
- **Returns:** True if successful, False on error

### `view() -> List[Tuple]`
Retrieve all books from the database.

### `search(title="", author="", year=None, isbn="") -> List[Tuple]`
Search for books with multiple criteria (AND logic).

### `delete(book_id) -> bool`
Delete a book by ID.

### `update(book_id, title, author, year, isbn) -> bool`
Update an existing book record.

### `get_book_by_id(book_id) -> Optional[Tuple]`
Retrieve a specific book by ID.

### `get_total_books() -> int`
Get total number of books in database.

## 🧪 Testing

Run tests with pytest:

```bash
pytest tests/ -v
```

## 🚀 Future Improvements

- [ ] Add database migration system
- [ ] Implement user authentication
- [ ] Create REST API with Flask/FastAPI
- [ ] Add GUI with Tkinter or PyQt
- [ ] Add database backup functionality
- [ ] Implement advanced search filters
- [ ] Add book ratings and reviews
- [ ] Create web interface

## 📝 Recent Changes

### v2.0 (June 23, 2026)
- Fixed SQL syntax error (PRIMERY → PRIMARY KEY)
- Refactored with context managers for better resource handling
- Added comprehensive type hints and docstrings
- Improved error handling and validation
- Added LIKE queries for flexible searching
- Added helper functions (get_book_by_id, get_total_books)

## 📄 License

MIT License

## 👤 Author

**Amirmahdimanaseir**

---

**Note:** This is a learning project demonstrating database management best practices.
