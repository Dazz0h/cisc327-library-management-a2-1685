# Library Management System - Assignment 2

https://github.com/OWNER/REPOSITORY/actions/workflows/WORKFLOW-FILE/badge.svg

## Overview
A comprehensive Library Management System built with Flask and Python, featuring complete business logic implementation, extensive test coverage, and automated CI/CD pipeline.

## Features
- **Book Catalog Management**: Add, search, and manage books with comprehensive validation
- **Borrowing System**: Patron book borrowing with limits and due date tracking
- **Return Processing**: Book return handling with late fee calculation
- **Search Functionality**: Advanced search by title, author, and ISBN
- **Patron Status Reports**: Comprehensive patron borrowing history and status
- **Late Fee Calculation**: Automated late fee calculation with configurable rates

## Business Logic Functions (Requirements R1-R7)
- **R1**: `add_book_to_catalog()` - Add new books with validation
- **R2**: Book catalog management (integrated with R1)
- **R3**: `borrow_book_by_patron()` - Handle book borrowing
- **R4**: `return_book_by_patron()` - Process book returns
- **R5**: `calculate_late_fee_for_book()` - Calculate late fees
- **R6**: `search_books_in_catalog()` - Search functionality
- **R7**: `get_patron_status_report()` - Patron status reporting

## Test Coverage
- **Human-Written Tests**: 24 comprehensive tests
- **AI-Generated Tests**: 64 advanced tests with edge cases
- **Total Coverage**: 88 tests covering all functionality
- **Test Types**: Unit tests, integration tests, edge case testing, boundary testing

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/[username]/cisc327-library-management-a2-[student-id].git
   cd cisc327-library-management-a2-[student-id]
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the application at: `http://localhost:5000`

## Running Tests

### Run All Tests
```bash
pytest tests/ ai_generated_tests.py -v
```

### Run Human-Written Tests Only
```bash
pytest tests/ -v
```

### Run AI-Generated Tests Only
```bash
pytest ai_generated_tests.py -v
```

### Run with Coverage Report
```bash
pytest tests/ ai_generated_tests.py --cov=. --cov-report=html
```

## CI/CD Pipeline

This project includes a comprehensive GitHub Actions workflow that:

- **Multi-Python Testing**: Tests on Python 3.8, 3.9, 3.10, 3.11, and 3.12
- **Code Quality**: Runs flake8 linting and code style checks
- **Security Scanning**: Bandit security analysis and safety dependency checks
- **Performance Testing**: Automated performance benchmarks
- **Coverage Reporting**: Code coverage analysis with Codecov integration
- **Build Verification**: Application health checks and artifact generation

### Workflow Triggers
- **Push to main/master**: Full pipeline execution
- **Pull Requests**: Test and quality checks
- **Manual**: Can be triggered manually from GitHub Actions tab

## Project Structure
```
├── app.py                          # Main Flask application
├── library_service.py              # Core business logic
├── database.py                     # Database operations
├── routes/                         # Flask route handlers
│   ├── api_routes.py
│   ├── borrowing_routes.py
│   ├── catalog_routes.py
│   └── search_routes.py
├── templates/                      # HTML templates
├── tests/                          # Human-written test suite
│   ├── test_add_book.py
│   ├── test_borrow_book.py
│   ├── test_late_fee.py
│   ├── test_patron_status.py
│   ├── test_return_book.py
│   └── test_search_books.py
├── ai_generated_tests.py           # AI-generated comprehensive tests
├── test_comparison_analysis.md     # Detailed test comparison report
├── .github/workflows/              # CI/CD pipeline configuration
└── requirements.txt                # Python dependencies
```

## API Documentation

### Book Management
- **Add Book**: `POST /api/books` - Add new book to catalog
- **Search Books**: `GET /api/books/search` - Search books by various criteria
- **Get All Books**: `GET /api/books` - Retrieve all books

### Borrowing Operations
- **Borrow Book**: `POST /api/borrow` - Borrow a book
- **Return Book**: `POST /api/return` - Return a borrowed book
- **Calculate Late Fee**: `GET /api/late-fee` - Calculate late fees

### Patron Management
- **Patron Status**: `GET /api/patron/status` - Get patron status report

## Test Comparison Results

### Human-Written Tests
- **Count**: 24 tests
- **Coverage**: Basic functionality and validation
- **Strengths**: Simple, maintainable, focused
- **Areas**: Core functionality, basic edge cases

### AI-Generated Tests
- **Count**: 64 tests
- **Coverage**: Comprehensive edge cases and integration
- **Strengths**: Extensive coverage, boundary testing, integration workflows
- **Areas**: Advanced validation, complex business logic, error scenarios

### Combined Results
- **Total Tests**: 88 tests
- **Pass Rate**: 100%
- **Coverage**: All business logic functions thoroughly tested

## Security Features
- Input validation and sanitization
- SQL injection prevention
- XSS protection in templates
- Dependency vulnerability scanning
- Code security analysis with Bandit

## Performance
- Optimized database queries
- Efficient search algorithms
- Connection pooling
- Automated performance testing in CI/CD

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License
This project is part of CISC/CMPE 327 coursework at Queen's University.

## Assignment 2 Completion Status
✅ **Function Implementation**: All business logic functions completed  
✅ **Test Suite Development**: Comprehensive test coverage achieved  
✅ **AI-Assisted Test Generation**: 64 advanced tests generated  
✅ **Test Comparison Analysis**: Detailed comparison completed  
✅ **CI/CD Pipeline Setup**: GitHub Actions workflow configured  
