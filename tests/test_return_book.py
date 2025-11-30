import pytest
from library_service import return_book_by_patron, add_book_to_catalog, borrow_book_by_patron
from database import get_book_by_isbn

# R4: Return Book
def test_return_book_not_borrowed():
    success, message = return_book_by_patron("999999", 99999)
    assert success is False
    assert "no active borrow record" in message.lower() or "not found" in message.lower()

def test_return_book_valid():
    add_book_to_catalog("Returnable Book", "Author", "5555555555557", 1)
    book = get_book_by_isbn("5555555555557")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("111111", book_id)
    success, message = return_book_by_patron("111111", book_id)
    assert success is True
    assert "book returned" in message.lower()

def test_return_book_invalid_patron():
    add_book_to_catalog("Test Book", "Author", "6666666666668", 1)
    book = get_book_by_isbn("6666666666668")
    assert book is not None
    book_id = book['id']
    success, message = return_book_by_patron("abc", book_id)
    assert success is False
    assert "6 digits" in message

def test_return_book_already_returned():
    add_book_to_catalog("Already Returned Book", "Author", "7777777777779", 1)
    book = get_book_by_isbn("7777777777779")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("222222", book_id)
    return_book_by_patron("222222", book_id)  # First return
    success, message = return_book_by_patron("222222", book_id)  # Second return
    assert success is False
    assert "no active borrow record" in message.lower() or "not found" in message.lower()
