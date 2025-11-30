@echo off
echo ========================================
echo  Assignment 4 - E2E Test Runner
echo ========================================
echo.

echo Current directory: %cd%
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo Installing Playwright browsers...
playwright install chromium
echo.

echo Running E2E tests...
pytest tests/test_e2e.py -v --tb=short
echo.

echo ========================================
echo  Tests Complete!
echo ========================================
echo.
pause
