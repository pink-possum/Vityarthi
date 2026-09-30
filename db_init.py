import csv
import os
from config import BOOKS_FILE, MEMBERS_FILE, TRANSACTIONS_FILE

def setup_storage_files():
    """Creates the required CSV files with headers if they do not exist."""
    if not os.path.exists(BOOKS_FILE):
        with open(BOOKS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['book_id', 'isbn', 'title', 'author', 'publisher', 'year', 'total_copies', 'available_copies'])
            
    if not os.path.exists(MEMBERS_FILE):
        with open(MEMBERS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['member_id', 'name', 'class', 'contact'])
            
    if not os.path.exists(TRANSACTIONS_FILE):
        with open(TRANSACTIONS_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['trans_id', 'book_id', 'member_id', 'issue_date', 'due_date', 'return_date', 'fine'])