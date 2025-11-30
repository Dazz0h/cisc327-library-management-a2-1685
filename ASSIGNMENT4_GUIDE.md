# Assignment 4 Implementation Guide

## Files Created

1. **tests/test_e2e.py** - End-to-End browser tests using Playwright
2. **Dockerfile** - Container configuration for the Flask app
3. **requirements.txt** - Updated with Playwright dependencies

## Task 1: Browser-Based E2E Testing

### Installation Steps

1. Install the updated dependencies:
```bash
pip install -r requirements.txt
```

2. Install Playwright browsers:
```bash
playwright install chromium
```

### Running E2E Tests

Run all E2E tests:
```bash
pytest tests/test_e2e.py -v
```

Run with visible browser (non-headless):
```bash
pytest tests/test_e2e.py -v --headed
```

### Test Coverage

The E2E tests cover the following user flows:

1. **test_add_book_and_verify_in_catalog**
   - Navigate to add book page
   - Fill in book details (title, author, ISBN, copies)
   - Submit the form
   - Verify book appears in catalog with correct details

2. **test_borrow_book_complete_flow**
   - Navigate to catalog
   - Find available book
   - Enter patron ID and borrow book
   - Verify success message
   - Verify available copies decreased

3. **test_navigation_and_ui_elements**
   - Test navigation between pages
   - Verify UI elements exist
   - Test cancel functionality

4. **test_add_book_validation**
   - Verify form validation
   - Check required fields
   - Verify field constraints

## Task 2: Application Containerization

### Building the Docker Image

```bash
docker build -t library-app .
```

### Running the Container

```bash
docker run -p 5000:5000 library-app
```

### Accessing the Application

Open your browser and navigate to: http://localhost:5000

### Stopping the Container

Press `Ctrl+C` or find the container ID and stop it:
```bash
docker ps
docker stop <container_id>
```

## Task 3: Docker Hub Deployment

### Prerequisites
- Create a Docker Hub account at https://hub.docker.com

### Login to Docker Hub

```bash
docker login
```

### Tag the Image

Replace `yourdockerhubusername` with your actual Docker Hub username:
```bash
docker tag library-app yourdockerhubusername/library-app:v1
```

### Push to Docker Hub

```bash
docker push yourdockerhubusername/library-app:v1
```

### Delete Local Image

```bash
docker rmi yourdockerhubusername/library-app:v1
docker rmi library-app
```

### Pull from Docker Hub

```bash
docker pull yourdockerhubusername/library-app:v1
```

### Run the Pulled Image

```bash
docker run -p 5000:5000 yourdockerhubusername/library-app:v1
```

## Screenshots Needed for Report

Take screenshots of:

1. **E2E Tests**
   - Terminal showing successful test execution
   - All 4 tests passing

2. **Docker Build**
   - Terminal showing `docker build` command and successful completion
   - Docker images list showing the built image

3. **Docker Run**
   - Terminal showing `docker run` command
   - Browser showing the app running at localhost:5000

4. **Docker Hub Push**
   - Terminal showing successful `docker push`
   - Docker Hub web interface showing the image

5. **Docker Hub Pull**
   - Terminal showing `docker rmi` (delete)
   - Terminal showing `docker pull`
   - Terminal showing `docker run` with pulled image

## Troubleshooting

### Issue: Port 5000 already in use
**Solution:** Stop any running Flask apps or change the port:
```bash
docker run -p 5001:5000 library-app
```

### Issue: E2E tests fail with "Port already in use"
**Solution:** Stop the Flask app before running tests, or the tests will skip automatically

### Issue: Playwright browsers not installed
**Solution:** Run:
```bash
playwright install chromium
```

### Issue: Database issues in Docker
**Solution:** The app automatically initializes the SQLite database on startup. If issues persist, rebuild the image:
```bash
docker build --no-cache -t library-app .
```

## Report Structure

Your PDF report should include:

1. **Student Information** (name, ID, date)
2. **E2E Testing Approach**
   - Tool used: Playwright (Python)
   - Features tested: Add book, borrow book, navigation, validation
   - Assertions: UI elements, text content, availability changes
3. **Execution Instructions**
   - Commands to install dependencies
   - Commands to run tests
   - Commands to build and run container
4. **Test Case Summary** (table format)

| Test Case | Actions | Expected Results | Status |
|-----------|---------|-----------------|--------|
| Add Book Flow | Navigate to add book, fill form, submit | Book appears in catalog | Pass |
| Borrow Book Flow | Find book, enter patron ID, borrow | Success message, availability decreased | Pass |
| Navigation | Click links, navigate pages | Correct pages load | Pass |
| Validation | Check form constraints | Required fields enforced | Pass |

5. **Dockerization Process**
   - Dockerfile explanation
   - Build command and screenshot
   - Run command and screenshot
   - Browser screenshot of running app

6. **Docker Hub Deployment**
   - Push screenshot
   - Delete screenshot
   - Pull screenshot
   - Run screenshot

7. **Challenges and Reflections**
   - Any difficulties encountered
   - What you learned about E2E testing and containerization

## Additional Notes

- The Flask app runs on port 5000 by default
- The SQLite database (library.db) is created automatically
- Sample data is added on first run
- All tests use headless browser mode by default for CI/CD compatibility
- Docker image size should be under 500MB (current setup uses python:3.11-slim)

## File Structure Check

Ensure your repository has this structure:

```
/
├── tests/
│   ├── test_e2e.py          (NEW - E2E tests)
│   ├── conftest.py
│   └── ... (other test files)
├── routes/
│   └── ... (route files)
├── templates/
│   └── ... (HTML files)
├── app.py
├── database.py
├── library_service.py
├── Dockerfile               (NEW)
├── requirements.txt         (UPDATED)
└── README.md
```

## Good Luck!

If you encounter any issues, refer to:
- Playwright documentation: https://playwright.dev/python/
- Docker documentation: https://docs.docker.com/
- Flask documentation: https://flask.palletsprojects.com/
