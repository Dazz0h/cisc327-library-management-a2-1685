"""
Library Service Module - Business Logic Functions
Contains all the core business logic for the Library Management System
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database import (
    get_book_by_id, get_book_by_isbn, get_patron_borrow_count,
    insert_book, insert_borrow_record, update_book_availability,
    update_borrow_record_return_date, get_all_books
)

def add_book_to_catalog(title: str, author: str, isbn: str, total_copies: int) -> Tuple[bool, str]:
    """
    Add a new book to the catalog.
    Implements R1: Book Catalog Management
    
    Args:
        title: Book title (max 200 chars)
        author: Book author (max 100 chars)
        isbn: 13-digit ISBN
        total_copies: Number of copies (positive integer)
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Input validation
    if not title or not title.strip():
        return False, "Title is required."
    
    if len(title.strip()) > 200:
        return False, "Title must be less than 200 characters."
    
    if not author or not author.strip():
        return False, "Author is required."
    
    if len(author.strip()) > 100:
        return False, "Author must be less than 100 characters."
    
    if len(isbn) != 13:
        return False, "ISBN must be exactly 13 digits."
    
    if not isbn.isdigit():
        return False, "ISBN must contain only digits."
    
    if not isinstance(total_copies, int) or total_copies <= 0:
        return False, "Total copies must be a positive integer."
    
    # Check for duplicate ISBN
    existing = get_book_by_isbn(isbn)
    if existing:
        return False, "A book with this ISBN already exists."
    
    # Insert new book
    success = insert_book(title.strip(), author.strip(), isbn, total_copies, total_copies)
    if success:
        return True, f'Book "{title.strip()}" has been successfully added to the catalog.'
    else:
        return False, "Database error occurred while adding the book."

def borrow_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Allow a patron to borrow a book.
    Implements R3 as per requirements  
    
    Args:
        patron_id: 6-digit library card ID
        book_id: ID of the book to borrow
        
    Returns:
        tuple: (success: bool, message: str)
    """
    # Validate patron ID
    if not patron_id or not isinstance(patron_id, str) or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    
    # Check if book exists and is available
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    
    if book['available_copies'] <= 0:
        return False, "This book is currently not available."
    
    # Check patron's current borrowed books count
    current_borrowed = get_patron_borrow_count(patron_id)
    
    if current_borrowed >= 5:
        return False, "You have reached the maximum borrowing limit of 5 books."
    
    # Create borrow record
    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=14)
    
    # Insert borrow record and update availability
    borrow_success = insert_borrow_record(patron_id, book_id, borrow_date, due_date)
    if not borrow_success:
        return False, "Database error occurred while creating borrow record."
    
    availability_success = update_book_availability(book_id, -1)
    if not availability_success:
        return False, "Database error occurred while updating book availability."
    
    return True, f'Successfully borrowed "{book["title"]}". Due date: {due_date.strftime("%Y-%m-%d")}.'

def return_book_by_patron(patron_id: str, book_id: int) -> Tuple[bool, str]:
    """
    Process book return by a patron.
    Implements R4: Book Return Processing
    """
    # Validate patron ID
    if not patron_id or not isinstance(patron_id, str) or not patron_id.isdigit() or len(patron_id) != 6:
        return False, "Invalid patron ID. Must be exactly 6 digits."
    # Check if book exists
    book = get_book_by_id(book_id)
    if not book:
        return False, "Book not found."
    # Check if the book was borrowed by the patron and not yet returned
    from database import get_borrow_record
    record = get_borrow_record(patron_id, book_id)
    if not record or record['return_date'] is not None:
        return False, "No active borrow record found for this patron and book."
    # Update borrow record with return date
    now = datetime.now()
    updated = update_borrow_record_return_date(patron_id, book_id, now)
    if not updated:
        return False, "Database error occurred while updating return date."
    # Increment book availability
    avail_updated = update_book_availability(book_id, 1)
    if not avail_updated:
        return False, "Database error occurred while updating book availability."
    # Calculate late fee (optional, for message)
    due_date = record['due_date']
    days_late = (now - due_date).days
    if days_late > 0:
        return True, f'Book returned. You are {days_late} days late.'
    else:
        return True, 'Book returned on time. Thank you!'

def calculate_late_fee_for_book(patron_id: str, book_id: int) -> Dict:
    """
    Calculate late fees for a specific book.
    Implements R5: Late Fee Calculation API
    """
    from database import get_borrow_record
    record = get_borrow_record(patron_id, book_id)
    if not record:
        return {
            'fee_amount': 0.00,
            'days_overdue': 0,
            'status': 'No borrow record found.'
        }
    due_date = record['due_date']
    return_date = record['return_date'] or datetime.now()
    days_overdue = (return_date - due_date).days
    if days_overdue <= 0:
        return {
            'fee_amount': 0.00,
            'days_overdue': 0,
            'status': 'No late fee.'
        }
    # Calculate fee
    fee = 0.0
    if days_overdue <= 7:
        fee = days_overdue * 0.5
    else:
        fee = 7 * 0.5 + (days_overdue - 7) * 1.0
    fee = min(fee, 15.0)
    return {
        'fee_amount': round(fee, 2),
        'days_overdue': days_overdue,
        'status': 'Late fee applied.'
    }

def search_books_in_catalog(search_term: str, search_type: str) -> List[Dict]:
    """
    Search for books in the catalog.
    Implements R6: Book Search Functionality
    """
    from database import get_all_books
    books = get_all_books()
    term = search_term.strip().lower()
    results = []
    
    # Return empty results for empty search terms
    if not term:
        return results
    
    if search_type == 'title':
        results = [b for b in books if term in b['title'].lower()]
    elif search_type == 'author':
        results = [b for b in books if term in b['author'].lower()]
    elif search_type == 'isbn':
        results = [b for b in books if b['isbn'] == search_term.strip()]
    else:
        results = []
    return results

def get_patron_status_report(patron_id: str) -> Dict:
    """
    Get status report for a patron.
    Implements R7: Patron Status Report
    """
    from database import get_patron_borrowed_books, get_patron_borrow_count, get_db_connection
    # Currently borrowed books
    borrowed_books = get_patron_borrowed_books(patron_id)
    # Number of books currently borrowed
    num_borrowed = get_patron_borrow_count(patron_id)
    # Borrowing history (all books ever borrowed)
    conn = get_db_connection()
    history_records = conn.execute('''
        SELECT br.*, b.title, b.author FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        WHERE br.patron_id = ?
        ORDER BY br.borrow_date DESC
    ''', (patron_id,)).fetchall()
    conn.close()
    history = []
    total_late_fees = 0.0
    for record in history_records:
        due_date = datetime.fromisoformat(record['due_date'])
        return_date = datetime.fromisoformat(record['return_date']) if record['return_date'] else None
        days_overdue = 0
        fee = 0.0
        if return_date and return_date > due_date:
            days_overdue = (return_date - due_date).days
        elif not return_date and datetime.now() > due_date:
            days_overdue = (datetime.now() - due_date).days
        if days_overdue > 0:
            if days_overdue <= 7:
                fee = days_overdue * 0.5
            else:
                fee = 7 * 0.5 + (days_overdue - 7) * 1.0
            fee = min(fee, 15.0)
        total_late_fees += fee
        history.append({
            'book_id': record['book_id'],
            'title': record['title'],
            'author': record['author'],
            'borrow_date': record['borrow_date'],
            'due_date': record['due_date'],
            'return_date': record['return_date'],
            'late_fee': round(fee, 2),
            'days_overdue': days_overdue
        })
    return {
        'currently_borrowed': borrowed_books,
        'num_borrowed': num_borrowed,
        'total_late_fees': round(total_late_fees, 2),
        'borrowing_history': history
    }
