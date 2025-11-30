import pytest
from library_service import add_book_to_catalog, search_books_in_catalog

# R6: Search Books
def test_search_books_by_title():
    add_book_to_catalog("UniqueTitleBook", "Author", "6666666666680", 1)
    results = search_books_in_catalog("UniqueTitleBook", "title")
    assert any("UniqueTitleBook" in b['title'] for b in results)

def test_search_books_by_author():
    add_book_to_catalog("BookA", "SpecialAuthor", "7777777777781", 1)
    results = search_books_in_catalog("SpecialAuthor", "author")
    assert any("SpecialAuthor" in b['author'] for b in results)

def test_search_books_by_isbn():
    add_book_to_catalog("BookB", "AuthorB", "8888888888882", 1)
    results = search_books_in_catalog("8888888888882", "isbn")
    assert any(b['isbn'] == "8888888888882" for b in results)

def test_search_books_no_results():
    results = search_books_in_catalog("NonExistentBook", "title")
    assert len(results) == 0