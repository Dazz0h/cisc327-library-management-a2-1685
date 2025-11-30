@echo off
echo ========================================
echo  Git Setup and Push to GitHub
echo ========================================
echo.

echo Step 1: Initializing Git repository...
git init
echo.

echo Step 2: Adding all files...
git add .
echo.

echo Step 3: Creating commit...
git commit -m "Add Assignment 4: E2E Testing and Docker Containerization

- Implement browser-based E2E tests using Playwright
  * Add book and verify in catalog flow
  * Borrow book complete flow
  * Navigation and UI elements testing
  * Form validation testing

- Create Dockerfile for application containerization
  * Use Python 3.11-slim base image
  * Expose port 5000
  * Include SQLite database initialization

- Update requirements.txt with Playwright dependencies
- Add pytest.ini for test configuration
- Create helper scripts for testing and Docker build
- Add comprehensive assignment guide documentation"

echo.

echo Step 4: Adding remote repository...
git remote add origin https://github.com/Dazz0h/cisc327-library-management-a2-1685.git
echo.

echo Step 5: Renaming branch to main...
git branch -M main
echo.

echo Step 6: Pushing to GitHub...
git push -u origin main --force
echo.

echo ========================================
echo  Push Complete!
echo ========================================
echo.
echo Visit: https://github.com/Dazz0h/cisc327-library-management-a2-1685
echo.
pause
