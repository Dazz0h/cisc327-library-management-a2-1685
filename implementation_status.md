# Implementation Status Document

## Project: Library Management System (CISC/CMPE 327, Fall 2025)

### 1. Project Setup
- Cloned/downloaded the project from the provided GitHub repository.
- Installed all dependencies using `pip install -r requirements.txt`.
- Initialized the database and added sample data.
- Successfully ran the Flask web application and accessed it in the browser at `http://localhost:5000`.

### 2. Issues Encountered & Solutions
- No major issues encountered during setup.
- Minor: Ensured Python and pip were up to date for dependency installation.
- Implemented missing business logic functions for requirements R4–R7 in `library_service.py` and added a helper in `database.py` for borrow record lookup.
- Improved test reliability by dynamically fetching book IDs in tests, avoiding hardcoded IDs and duplicate ISBN issues.

### 3. Unit Test Coverage
- All business logic functions (R1–R7) in `library_service.py` are covered by unit tests in `sample_test.py`.
- Tests include both normal and edge/error cases for adding, borrowing, returning books, late fee calculation, searching, and patron status reports.
- Tests are written using `pytest` and can be run with the command:
  ```
  pytest sample_test.py
  ```
- Tests dynamically fetch book IDs after adding books to ensure robustness regardless of database state.

### 4. Current Status
- The web application runs successfully with all required features implemented.
- All business logic functions (R1–R7) are present and fully tested.
- Unit test scripts are included and pass (except for expected edge cases).
- Project is ready for submission as per assignment instructions.
