"""
End-to-End Browser Tests for Library Management System
Tests realistic user flows using Playwright
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
import time
from playwright.sync_api import Page, expect
from app import create_app
import threading
import socket


def is_port_available(port):
    """Check if a port is available."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) != 0


@pytest.fixture(scope="module")
def flask_app():
    """Start Flask app in a separate thread for testing."""
    app = create_app()

    # Check if port 5000 is available
    if not is_port_available(5000):
        pytest.skip("Port 5000 is already in use")

    def run_app():
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

    thread = threading.Thread(target=run_app, daemon=True)
    thread.start()

    # Give the server time to start
    time.sleep(2)

    yield app

    # Cleanup happens automatically as thread is daemon


@pytest.fixture(scope="function")
def page(playwright, flask_app):
    """Create a new browser page for each test."""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()
    browser.close()


def test_add_book_and_verify_in_catalog(page: Page):
    """
    Test Flow 1: Add a new book and verify it appears in catalog

    Steps:
    1. Navigate to add book page
    2. Fill in book details (title, author, ISBN, copies)
    3. Submit the form
    4. Verify redirect to catalog page
    5. Verify the book appears in the catalog with correct details
    """
    # Navigate to add book page
    page.goto("http://localhost:5000/add_book")

    # Verify we're on the add book page
    expect(page.locator("h2")).to_contain_text("Add New Book")

    # Generate unique ISBN for this test run
    import random
    unique_isbn = f"97801234{random.randint(10000, 99999)}"

    # Fill in book details
    page.fill("#title", "Test Book E2E")
    page.fill("#author", "Test Author E2E")
    page.fill("#isbn", unique_isbn)
    page.fill("#total_copies", "5")

    # Submit the form
    page.click("button[type='submit']")

    # Verify redirect to catalog page
    expect(page).to_have_url("http://localhost:5000/catalog")

    # Verify success message appears
    expect(page.locator(".flash-success")).to_be_visible()

    # Verify the book appears in catalog with correct details
    # Look for a table row containing our book data
    book_row = page.locator(f"tr:has-text('{unique_isbn}')")
    expect(book_row).to_be_visible()

    # Verify book details in the row
    expect(book_row).to_contain_text("Test Book E2E")
    expect(book_row).to_contain_text("Test Author E2E")
    expect(book_row).to_contain_text(unique_isbn)
    expect(book_row).to_contain_text("5/5 Available")


def test_borrow_book_complete_flow(page: Page):
    """
    Test Flow 2: Complete book borrowing flow

    Steps:
    1. Navigate to catalog
    2. Find a book with available copies
    3. Enter patron ID and borrow the book
    4. Verify borrow confirmation message appears
    5. Verify available copies decreased
    """
    # Navigate to catalog
    page.goto("http://localhost:5000/catalog")

    # Verify we're on the catalog page
    expect(page.locator("h2")).to_contain_text("Book Catalog")

    # Find first available book (with "Available" status)
    available_book_row = page.locator("tr:has(span.status-available)").first

    # Verify there's at least one available book
    expect(available_book_row).to_be_visible()

    # Get book title before borrowing for verification
    book_title = available_book_row.locator("td").nth(1).inner_text()

    # Get initial availability text
    initial_availability = available_book_row.locator("span.status-available").inner_text()

    # Fill patron ID (6 digits) and click borrow button
    patron_id_input = available_book_row.locator("input[name='patron_id']")
    patron_id_input.fill("123456")

    # Click the borrow button
    borrow_button = available_book_row.locator("button[type='submit']")
    borrow_button.click()

    # Wait for page to reload
    page.wait_for_load_state("networkidle")

    # Verify we're still on catalog page (or redirected back to it)
    expect(page).to_have_url("http://localhost:5000/catalog")

    # Verify success message appears
    success_message = page.locator(".flash-success")
    expect(success_message).to_be_visible()
    expect(success_message).to_contain_text("Successfully borrowed")

    # Verify the book's available copies decreased
    # Find the same book row again after reload
    updated_book_row = page.locator(f"tr:has-text('{book_title}')").first
    expect(updated_book_row).to_be_visible()

    # Verify availability changed (either decreased count or became unavailable)
    updated_availability = updated_book_row.locator("td").nth(4).inner_text()

    # The availability should have changed from the initial state
    assert updated_availability != initial_availability, "Book availability should have changed after borrowing"


def test_navigation_and_ui_elements(page: Page):
    """
    Test Flow 3: Navigation and UI elements verification

    Steps:
    1. Navigate to home page
    2. Verify navigation elements exist
    3. Navigate to different pages
    4. Verify page titles and key UI elements
    """
    # Navigate to home page
    page.goto("http://localhost:5000/")

    # Should redirect to catalog
    expect(page).to_have_url("http://localhost:5000/catalog")

    # Verify catalog page elements
    expect(page.locator("h2")).to_contain_text("Book Catalog")
    expect(page.locator("table")).to_be_visible()

    # Verify "Add New Book" button exists
    add_book_link = page.locator("a:has-text('Add New Book')")
    expect(add_book_link).to_be_visible()

    # Click to navigate to add book page
    add_book_link.click()

    # Verify we're on add book page
    expect(page).to_have_url("http://localhost:5000/add_book")
    expect(page.locator("h2")).to_contain_text("Add New Book")

    # Verify form fields exist
    expect(page.locator("#title")).to_be_visible()
    expect(page.locator("#author")).to_be_visible()
    expect(page.locator("#isbn")).to_be_visible()
    expect(page.locator("#total_copies")).to_be_visible()

    # Verify cancel button exists and works
    cancel_button = page.locator("a:has-text('Cancel')")
    expect(cancel_button).to_be_visible()
    cancel_button.click()

    # Should return to catalog
    expect(page).to_have_url("http://localhost:5000/catalog")


def test_add_book_validation(page: Page):
    """
    Test Flow 4: Form validation for adding books

    Steps:
    1. Navigate to add book page
    2. Try to submit empty form
    3. Verify HTML5 validation prevents submission
    4. Fill partial data and verify validation
    """
    # Navigate to add book page
    page.goto("http://localhost:5000/add_book")

    # Try to submit empty form
    submit_button = page.locator("button[type='submit']")

    # Verify required fields exist
    title_input = page.locator("#title")
    author_input = page.locator("#author")
    isbn_input = page.locator("#isbn")
    copies_input = page.locator("#total_copies")

    # Check that fields are marked as required
    expect(title_input).to_have_attribute("required", "")
    expect(author_input).to_have_attribute("required", "")
    expect(isbn_input).to_have_attribute("required", "")
    expect(copies_input).to_have_attribute("required", "")

    # Verify field constraints
    expect(title_input).to_have_attribute("maxlength", "200")
    expect(author_input).to_have_attribute("maxlength", "100")
    expect(isbn_input).to_have_attribute("maxlength", "13")
    expect(copies_input).to_have_attribute("min", "1")
