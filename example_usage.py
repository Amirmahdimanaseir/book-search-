"""
Example usage of the Book Database System.
This demonstrates how to use all the available functions.
"""

from backend import (
    insert, view, search, update, delete, 
    get_book_by_id, get_total_books
)


def main():
    """Run example operations."""
    
    print("=" * 60)
    print("📚 Book Database System - Example Usage")
    print("=" * 60)
    
    # Example 1: Insert books
    print("\n1️⃣  Inserting books...")
    books_to_add = [
        ("Python Programming", "Guido van Rossum", 2020, "978-0134692011"),
        ("Clean Code", "Robert C. Martin", 2008, "978-0132350884"),
        ("Design Patterns", "Gang of Four", 1994, "978-0201633610"),
        ("Refactoring", "Martin Fowler", 2018, "978-0134757599"),
    ]
    
    for title, author, year, isbn in books_to_add:
        success = insert(title, author, year, isbn)
        if success:
            print(f"   ✓ Added: {title}")
        else:
            print(f"   ✗ Failed to add: {title}")
    
    # Example 2: View all books
    print("\n2️⃣  Viewing all books...")
    books = view()
    print(f"   Total books in database: {get_total_books()}")
    print("   All books:")
    for book in books:
        print(f"   - [{book[0]}] {book[1]} by {book[2]} ({book[3]})")
    
    # Example 3: Search by title
    print("\n3️⃣  Searching for books with 'Python' in title...")
    results = search(title="Python")
    for book in results:
        print(f"   - {book[1]} by {book[2]}")
    
    # Example 4: Search by author
    print("\n4️⃣  Searching for books by Martin Fowler...")
    results = search(author="Martin Fowler")
    for book in results:
        print(f"   - {book[1]} ({book[3]})")
    
    # Example 5: Search by year
    print("\n5️⃣  Searching for books published in 2018...")
    results = search(year=2018)
    for book in results:
        print(f"   - {book[1]} by {book[2]}")
    
    # Example 6: Get specific book
    print("\n6️⃣  Getting book with ID 1...")
    book = get_book_by_id(1)
    if book:
        print(f"   ID: {book[0]}")
        print(f"   Title: {book[1]}")
        print(f"   Author: {book[2]}")
        print(f"   Year: {book[3]}")
        print(f"   ISBN: {book[4]}")
    
    # Example 7: Update a book
    print("\n7️⃣  Updating book ID 2...")
    success = update(
        book_id=2,
        title="Clean Code: Advanced Techniques",
        author="Robert C. Martin",
        year=2021,
        isbn="978-0132350884"
    )
    if success:
        print("   ✓ Book updated successfully")
        updated_book = get_book_by_id(2)
        print(f"   New title: {updated_book[1]}")
    
    # Example 8: Multiple criteria search
    print("\n8️⃣  Searching for books by 'Martin' published after 2000...")
    results = search(author="Martin", year=2008)
    for book in results:
        print(f"   - {book[1]} ({book[3]})")
    
    # Example 9: Delete a book
    print("\n9️⃣  Deleting book with ID 4...")
    success = delete(4)
    if success:
        print("   ✓ Book deleted successfully")
        print(f"   Remaining books: {get_total_books()}")
    
    # Example 10: Final view
    print("\n🔟 Final list of all books...")
    books = view()
    for i, book in enumerate(books, 1):
        print(f"   {i}. {book[1]} by {book[2]} ({book[3]}) - ISBN: {book[4]}")
    
    print("\n" + "=" * 60)
    print("✅ Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
