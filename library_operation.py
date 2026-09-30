"""Module for handling book inventory operations like adding and searching."""
from db_init import read_data, write_data, get_next_id
from config import BOOKS_FILE
from tabulate import tabulate

def register_new_book():
    """Prompts user for book details and appends a new record to the CSV."""
    books = read_data(BOOKS_FILE)
    
    print("\n--- Enter New Book Details ---")
    book_isbn = input('Enter ISBN: ').strip()
    book_title = input('Enter Book Title: ').strip()
    book_author = input('Enter Author Name: ').strip()
    book_publisher = input('Enter Publisher: ').strip()
    publish_year = input('Enter Publication Year: ').strip()
    
    try:
        inventory_count = int(input('Enter Number of Copies: ').strip())
    except ValueError:
        print("[!] Invalid input. Please enter a valid number for copies.")
        return

    new_book = {
        'book_id': get_next_id(books, 'book_id'),
        'isbn': book_isbn,
        'title': book_title,
        'author': book_author,
        'publisher': book_publisher,
        'year': publish_year,
        'total_copies': inventory_count,
        'available_copies': inventory_count
    }
    
    books.append(new_book)
    write_data(BOOKS_FILE, list(new_book.keys()), books)
    print(f"[+] Successfully added '{book_title}' to the catalog.")

def lookup_books():
    """Searches the CSV data for books matching a keyword in title, author, or ISBN."""
    books = read_data(BOOKS_FILE)
    search_keyword = input('\nEnter search term (Title, Author, or ISBN): ').strip().lower()
    
    query_results = []
    for b in books:
        if search_keyword in b['title'].lower() or search_keyword in b['author'].lower() or search_keyword in b['isbn'].lower():
            query_results.append([b['book_id'], b['isbn'], b['title'], b['author'], b['available_copies']])
            
    if query_results:
        print("\n--- Search Results ---")
        print(tabulate(query_results, headers=['Record ID', 'ISBN', 'Book Title', 'Author', 'In Stock']))
    else:
        print("[-] No matching books found in the catalog.")