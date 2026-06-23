"""
Configuration and constants for the Book Database System
"""

import os
from pathlib import Path

# Database Configuration
DATABASE_NAME = os.getenv("DB_NAME", "books.db")
DATABASE_DIR = Path(__file__).parent
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# Validation Constraints
BOOK_CONSTRAINTS = {
    "title": {
        "min_length": 1,
        "max_length": 255,
        "required": True
    },
    "author": {
        "min_length": 1,
        "max_length": 255,
        "required": True
    },
    "year": {
        "min_value": 1000,
        "max_value": 2100,
        "required": False
    },
    "isbn": {
        "min_length": 10,
        "max_length": 20,
        "required": False
    }
}

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = DATABASE_DIR / "app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
LOG_BACKUP_COUNT = 5

# Database Schema
BOOK_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS book (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL CHECK(length(trim(title)) > 0),
    author TEXT NOT NULL CHECK(length(trim(author)) > 0),
    year INTEGER CHECK(year IS NULL OR (year BETWEEN 1000 AND 2100)),
    isbn TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

# Database Indexes
DB_INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_title ON book(title)",
    "CREATE INDEX IF NOT EXISTS idx_author ON book(author)",
    "CREATE INDEX IF NOT EXISTS idx_isbn ON book(isbn)",
    "CREATE INDEX IF NOT EXISTS idx_year ON book(year)"
]

# Search Configuration
DEFAULT_SEARCH_LIMIT = 1000
MAX_SEARCH_LIMIT = 10000
