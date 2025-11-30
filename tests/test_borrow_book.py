import pytest
from library_service import add_book_to_catalog, borrow_book_by_patron
from database import get_book_by_isbn

# R3: Borrow Book
def test_borrow_book_valid():
    add_book_to_catalog("Borrowable Book", "Author", "2222222222223", 2)
    book = get_book_by_isbn("2222222222223")
    assert book is not None
    book_id = book['id']
    success, message = borrow_book_by_patron("123456", book_id)
    assert success is True or "already" in message.lower()

def test_borrow_book_invalid_patron():
    add_book_to_catalog("Another Book", "Author", "3333333333334", 1)
    book = get_book_by_isbn("3333333333334")
    assert book is not None
    book_id = book['id']
    success, message = borrow_book_by_patron("abc", book_id)
    assert success is False
    assert "6 digits" in message

def test_borrow_book_unavailable():
    add_book_to_catalog("Unavailable Book", "Author", "4444444444445", 1)
    book = get_book_by_isbn("4444444444445")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("654321", book_id)
    success, message = borrow_book_by_patron("654321", book_id)
    assert success is False
    assert "not available" in message.lower()

def test_borrow_book_nonexistent_book():
    success, message = borrow_book_by_patron("123456", 99999)
    assert success is False
    assert "not found" in message.lower() or "invalid" in message.lower()