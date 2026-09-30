"""Module for managing the checkout, return, and reporting of library assets."""
from db_init import read_data, write_data, get_next_id
from config import BOOKS_FILE, MEMBERS_FILE, TRANSACTIONS_FILE, DAILY_OVERDUE_PENALTY
from datetime import datetime, timedelta
from tabulate import tabulate

def process_book_issue():
    """Handles the logic for borrowing a book, verifying stock, and setting due dates."""
    books = read_data(BOOKS_FILE)
    transactions = read_data(TRANSACTIONS_FILE)
    
    print("\n----- Issue a Book ------")
    target_member_id = input('Enter Member ID: ').strip()
    target_book_id = input('Enter Book ID: ').strip()
    
    current_date = datetime.now().date()
    calculated_due_date = current_date + timedelta(days=14)
    
    book_index = next((i for i, b in enumerate(books) if b['book_id'] == target_book_id), -1)
    
    if book_index == -1:
        print("[-] Error: Book ID not found in the system.")
        return
        
    book_record = books[book_index]
    
    if int(book_record['available_copies']) <= 0:
        print(f"[-] Error: All copies of '{book_record['title']}' are currently checked out.")
        return
        
    confirmation = input(f"Issue '{book_record['title']}' to Member {target_member_id}? (y/n): ").strip().lower()
    if confirmation == 'y':
        new_transaction = {
            'trans_id': get_next_id(transactions, 'trans_id'),
            'book_id': target_book_id,
            'member_id': target_member_id,
            'issue_date': str(current_date),
            'due_date': str(calculated_due_date),
            'return_date': '',
            'fine': '0.00'
        }
        
        books[book_index]['available_copies'] = str(int(book_record['available_copies']) - 1)
        transactions.append(new_transaction)
        
        write_data(BOOKS_FILE, list(books[0].keys()), books)
        write_data(TRANSACTIONS_FILE, list(new_transaction.keys()), transactions)
        
        print(f"[+] Success! Book issued. Please return by: {calculated_due_date}")
    else:
        print("[-] Issue cancelled by user.")

def process_book_return():
    """Handles book returns, updates inventory, and calculates overdue penalties."""
    books = read_data(BOOKS_FILE)
    transactions = read_data(TRANSACTIONS_FILE)
    
    print("\n----- Return a Book -----")
    active_transaction_id = input('Enter Transaction ID: ').strip()
    
    trans_index = next((i for i, t in enumerate(transactions) if t['trans_id'] == active_transaction_id and not t['return_date']), -1)
    
    if trans_index == -1:
        print("[-] Error: No active transaction found with that ID.")
        return
        
    transaction_record = transactions[trans_index]
    current_date = datetime.now().date()
    expected_due_date = datetime.strptime(transaction_record['due_date'], "%Y-%m-%d").date()
    
    days_overdue = (current_date - expected_due_date).days
    penalty_amount = 0.0
    
    if days_overdue > 0:
        penalty_amount = days_overdue * DAILY_OVERDUE_PENALTY
        print(f"[!] Note: Book is {days_overdue} days overdue. Penalty applied.")

    confirmation = input(f"Confirm return and apply penalty of Rs {penalty_amount:.2f}? (y/n): ").strip().lower()
    if confirmation == 'y':
        transactions[trans_index]['return_date'] = str(current_date)
        transactions[trans_index]['fine'] = f"{penalty_amount:.2f}"
        
        book_index = next((i for i, b in enumerate(books) if b['book_id'] == transaction_record['book_id']), -1)
        if book_index != -1:
            books[book_index]['available_copies'] = str(int(books[book_index]['available_copies']) + 1)
            write_data(BOOKS_FILE, list(books[0].keys()), books)
            
        write_data(TRANSACTIONS_FILE, list(transactions[0].keys()), transactions)
        print(f"[+] Book successfully returned. Total fine collected: Rs {penalty_amount:.2f}")
    else:
        print("[-] Return cancelled by user.")

def generate_system_reports():
    """Fetches and displays requested data tables using CSV joins."""
    books = {b['book_id']: b for b in read_data(BOOKS_FILE)}
    members = {m['member_id']: m for m in read_data(MEMBERS_FILE)}
    transactions = read_data(TRANSACTIONS_FILE)
    
    print("\n----- Generate Reports -----")
    print("1. View Available Inventory")
    print("2. View All Active Loans")
    print("3. View Overdue Loans")
    report_selection = input('Select report type (1-3): ').strip()
    
    if report_selection == '1':
        inventory_results = [[b['book_id'], b['title'], b['available_copies']] for b in books.values() if int(b['available_copies']) > 0]
        print("\n" + tabulate(inventory_results, headers=['Book ID', 'Book Title', 'Copies Available']))
        
    elif report_selection == '2':
        active_loans = []
        for t in transactions:
            if not t['return_date']:
                b_title = books.get(t['book_id'], {}).get('title', 'Unknown')
                m_name = members.get(t['member_id'], {}).get('name', 'Unknown')
                active_loans.append([t['trans_id'], b_title, m_name, t['issue_date'], t['due_date']])
        print("\n" + tabulate(active_loans, headers=['Transaction ID', 'Book Title', 'Borrower', 'Checkout Date', 'Due Date']))
        
    elif report_selection == '3':
        overdue_loans = []
        current_date = datetime.now().date()
        for t in transactions:
            if not t['return_date']:
                due_date = datetime.strptime(t['due_date'], "%Y-%m-%d").date()
                if due_date < current_date:
                    b_title = books.get(t['book_id'], {}).get('title', 'Unknown')
                    m_name = members.get(t['member_id'], {}).get('name', 'Unknown')
                    overdue_loans.append([t['trans_id'], b_title, m_name, t['due_date']])
        print("\n" + tabulate(overdue_loans, headers=['Transaction ID', 'Book Title', 'Borrower', 'Originally Due']))
        
    else:
        print("[-] Invalid report selection.")