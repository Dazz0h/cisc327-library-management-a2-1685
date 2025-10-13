"""
Pytest configuration and fixtures for the Library Management System tests.
"""

import pytest
from database import init_database, clear_test_data


@pytest.fixture(autouse=True)
def setup_test_database():
    """Ensure database is initialized before each test."""
    # Initialize database to create tables if they don't exist
    init_database()
    yield
    # Clean up after test
    clear_test_data()


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically clean up test data before each test."""
    # Clear test data before each test
    clear_test_data()
    yield
    # Clear test data after each test (cleanup)
    clear_test_data()
