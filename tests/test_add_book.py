import pytest
from library_service import add_book_to_catalog

# R1: Add Book To Catalog
def test_add_book_valid_input():
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890001", 5)
    assert success is True
    assert "successfully added" in message.lower()

def test_add_book_invalid_isbn_too_short():
    success, message = add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    assert success is False
    assert "13 digits" in message

def test_add_book_duplicate_isbn():
    add_book_to_catalog("Book1", "Author1", "1111111111112", 2)
    success, message = add_book_to_catalog("Book2", "Author2", "1111111111112", 3)
    assert success is False
    assert "already exists" in message.lower()

def test_add_book_invalid_isbn_too_long():
    success, message = add_book_to_catalog("Test Book", "Test Author", "12345678901234", 5)
    assert success is False
    assert "13 digits" in message