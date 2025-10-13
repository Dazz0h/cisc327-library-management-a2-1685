# Assignment 1 Project Implementation Status & Test Script Summary

**Student:** Emmanuel Davidsons  
**Student ID (last 4 digits):** 1685  
**Group Number:** [Your Group Number Here]

---

## Project Implementation Status

| Function Name                | Implementation Status | What is Missing (if any)         |
|------------------------------|----------------------|----------------------------------|
| add_book_to_catalog          | Complete             | None                             |
| borrow_book_by_patron        | Complete             | None                             |
| return_book_by_patron        | Complete             | None                             |
| calculate_late_fee_for_book  | Complete             | None                             |
| search_books_in_catalog      | Complete             | None                             |
| get_patron_status_report     | Complete             | None                             |

---

# Assignment 1 Test Script Summary

This document summarizes the unit test scripts created for the Library Management System assignment. Each test file corresponds to a major functional requirement as specified in the requirements specification.

---

## tests/test_add_book.py
- **Requirement:** R1 - Add Book To Catalog
- **Description:** Tests adding books with valid and invalid data, including:
  - Valid book addition
  - Invalid ISBN (too short)
  - Duplicate ISBN

## tests/test_borrow_book.py
- **Requirement:** R3 - Book Borrowing Interface
- **Description:** Tests borrowing books, including:
  - Valid borrow
  - Invalid patron ID
  - Borrowing unavailable books

## tests/test_return_book.py
- **Requirement:** R4 - Book Return Processing
- **Description:** Tests returning books, including:
  - Attempting to return a book not borrowed by the patron

## tests/test_late_fee.py
- **Requirement:** R5 - Late Fee Calculation
- **Description:** Tests late fee calculation, including:
  - No borrow record
  - No late fee when returned on time

## tests/test_search_books.py
- **Requirement:** R6 - Book Search Functionality
- **Description:** Tests searching for books by:
  - Title
  - Author
  - ISBN

## tests/test_patron_status.py
- **Requirement:** R7 - Patron Status Report
- **Description:** Tests patron status report, including:
  - Currently borrowed books
  - Number of books borrowed
  - Total late fees
  - Borrowing history

---

Each test file contains at least 3–5 test cases, covering both positive and negative scenarios as required. Please refer to the individual test files in the `tests` folder for detailed test logic and assertions.
