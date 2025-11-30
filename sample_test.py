import pytest
from library_service import (
    add_book_to_catalog,
    borrow_book_by_patron,
    return_book_by_patron,
    calculate_late_fee_for_book,
    search_books_in_catalog,
    get_patron_status_report
)
from database import get_book_by_isbn

# R1: Add Book To Catalog
def test_add_book_valid_input():
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890999", 5)
    assert success is True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    assert success is False
    assert "13 digits" in message

def test_add_book_duplicate_isbn():
    add_book_to_catalog("Book1", "Author1", "1111111111111", 2)
    success, message = add_book_to_catalog("Book2", "Author2", "1111111111111", 3)
    assert success is False
    assert "already exists" in message.lower()

# R3: Borrow Book
def test_borrow_book_valid():
    add_book_to_catalog("Borrowable Book", "Author", "2222222222222", 2)
    book = get_book_by_isbn("2222222222222")
    assert book is not None
    book_id = book['id']
    success, message = borrow_book_by_patron("123456", book_id)
    assert success is True or "already" in message.lower()

def test_borrow_book_invalid_patron():
    add_book_to_catalog("Another Book", "Author", "3333333333333", 1)
    book = get_book_by_isbn("3333333333333")
    assert book is not None
    book_id = book['id']
    success, message = borrow_book_by_patron("abc", book_id)
    assert success is False
    assert "6 digits" in message

def test_borrow_book_unavailable():
    add_book_to_catalog("Unavailable Book", "Author", "4444444444444", 1)
    book = get_book_by_isbn("4444444444444")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("654321", book_id)
    success, message = borrow_book_by_patron("654321", book_id)
    assert success is False
    assert "not available" in message.lower()

# R4: Return Book
def test_return_book_not_borrowed():
    success, message = return_book_by_patron("999999", 99999)
    assert success is False
    assert "no active borrow record" in message.lower() or "not found" in message.lower()

# R5: Late Fee Calculation
def test_late_fee_no_record():
    result = calculate_late_fee_for_book("999999", 99999)
    assert result['fee_amount'] == 0.0
    assert result['days_overdue'] == 0

def test_late_fee_no_late():
    add_book_to_catalog("Fee Book", "Author", "5555555555555", 1)
    book = get_book_by_isbn("5555555555555")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("111111", book_id)
    result = calculate_late_fee_for_book("111111", book_id)
    assert result['fee_amount'] == 0.0

# R6: Search Books
def test_search_books_by_title():
    add_book_to_catalog("UniqueTitleBook", "Author", "6666666666666", 1)
    results = search_books_in_catalog("UniqueTitleBook", "title")
    assert any("UniqueTitleBook" in b['title'] for b in results)

def test_search_books_by_author():
    add_book_to_catalog("BookA", "SpecialAuthor", "7777777777777", 1)
    results = search_books_in_catalog("SpecialAuthor", "author")
    assert any("SpecialAuthor" in b['author'] for b in results)

def test_search_books_by_isbn():
    add_book_to_catalog("BookB", "AuthorB", "8888888888888", 1)
    results = search_books_in_catalog("8888888888888", "isbn")
    assert any(b['isbn'] == "8888888888888" for b in results)

# R7: Patron Status Report
def test_patron_status_report():
    add_book_to_catalog("StatusBook", "Author", "9999999999999", 1)
    book = get_book_by_isbn("9999999999999")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("222222", book_id)
    report = get_patron_status_report("222222")
    assert 'currently_borrowed' in report
    assert 'num_borrowed' in report
    assert 'total_late_fees' in report
    assert 'borrowing_history' in report