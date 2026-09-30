"""Main file for the Library Management System application."""
from db_init import setup_storage_files
from library_operation import register_new_book, lookup_books
from members import register_new_member
from transactions import process_book_issue, process_book_return, generate_system_reports
import sys

def execute_main_menu():
    """Displays the primary user interface and routes user input to correct modules."""
    setup_storage_files()
    
    while True:
        print('\n=========================================')
        print('   Central Library Management Portal')
        print('=========================================')
        print('[1] Register New Book')
        print('[2] Search Catalog')
        print('[3] Register New Member')
        print('[4] Process Book Issue')
        print('[5] Process Book Return')
        print('[6] Generate Reports')
        print('[7] Shut Down System')
        
        menu_selection = input('\nSelect an operation (1-7): ').strip()
        
        if menu_selection == '1':
            register_new_book()
        elif menu_selection == '2':
            lookup_books()
        elif menu_selection == '3':
            register_new_member()
        elif menu_selection == '4':
            process_book_issue()
        elif menu_selection == '5':
            process_book_return()
        elif menu_selection == '6':
            generate_system_reports()
        elif menu_selection == '7':
            print('\nShutting down system. Goodbye!')
            sys.exit(0)
        else:
            print('\n[!] Invalid command. Please select a number between 1 and 7.')

if __name__ == '__main__':
    execute_main_menu()