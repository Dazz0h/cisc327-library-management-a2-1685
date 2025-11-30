"""
Pytest configuration and fixtures for the Library Management System tests.
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

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
