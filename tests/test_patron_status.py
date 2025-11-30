import pytest
from library_service import add_book_to_catalog, borrow_book_by_patron, get_patron_status_report
from database import get_book_by_isbn

# R7: Patron Status Report
def test_patron_status_report():
    add_book_to_catalog("StatusBook", "Author", "9999999999000", 1)
    book = get_book_by_isbn("9999999999000")
    assert book is not None
    book_id = book['id']
    borrow_book_by_patron("222222", book_id)
    report = get_patron_status_report("222222")
    assert 'currently_borrowed' in report
    assert 'num_borrowed' in report
    assert 'total_late_fees' in report
    assert 'borrowing_history' in report

def test_patron_status_no_borrows():
    report = get_patron_status_report("333333")
    assert 'currently_borrowed' in report
    assert 'num_borrowed' in report
    assert 'total_late_fees' in report
    assert 'borrowing_history' in report
    assert report['num_borrowed'] == 0

def test_patron_status_multiple_borrows():
    add_book_to_catalog("Book1", "Author1", "1111111111113", 2)
    add_book_to_catalog("Book2", "Author2", "2222222222224", 1)
    book1 = get_book_by_isbn("1111111111113")
    book2 = get_book_by_isbn("2222222222224")
    borrow_book_by_patron("444444", book1['id'])
    borrow_book_by_patron("444444", book2['id'])
    report = get_patron_status_report("444444")
    assert report['num_borrowed'] >= 2

def test_patron_status_invalid_patron():
    report = get_patron_status_report("abc")
    assert 'currently_borrowed' in report
    assert 'num_borrowed' in report
    assert 'total_late_fees' in report
    assert 'borrowing_history' in report