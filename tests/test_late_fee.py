import pytest
from library_service import add_book_to_catalog, calculate_late_fee_for_book, borrow_book_by_patron
from database import get_book_by_isbn

# R5: Late Fee Calculation
def test_late_fee_no_record():
    result = calculate_late_fee_for_book("999999", 99999)
    assert result['fee_amount'] == 0.0
    assert result['days_overdue'] == 0

def test_late_fee_no_late():
    add_book_to_catalog("Fee Book", "Author", "5555555555556", 1)
    book = get_book_by_isbn("5555555555556")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("111111", book_id)
    result = calculate_late_fee_for_book("111111", book_id)
    assert result['fee_amount'] == 0.0

def test_late_fee_with_late():
    add_book_to_catalog("Late Fee Book", "Author", "6666666666667", 1)
    book = get_book_by_isbn("6666666666667")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("333333", book_id)
    # Simulate a late return by modifying the borrow date (this would need to be implemented in the service)
    result = calculate_late_fee_for_book("333333", book_id)
    assert 'fee_amount' in result
    assert 'days_overdue' in result

def test_late_fee_invalid_patron():
    add_book_to_catalog("Test Book", "Author", "7777777777778", 1)
    book = get_book_by_isbn("7777777777778")
    assert book is not None
    book_id = book['id']
    result = calculate_late_fee_for_book("abc", book_id)
    assert result['fee_amount'] == 0.0
    assert result['days_overdue'] == 0
