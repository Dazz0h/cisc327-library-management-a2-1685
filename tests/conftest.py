"""
Pytest configuration and fixtures for the Library Management System tests.
"""

import pytest
from database import clear_test_data


@pytest.fixture(autouse=True)
def cleanup_test_data():
    """Automatically clean up test data before each test."""
    # Clear test data before each test
    clear_test_data()
    yield
    # Clear test data after each test (cleanup)
    clear_test_data()
