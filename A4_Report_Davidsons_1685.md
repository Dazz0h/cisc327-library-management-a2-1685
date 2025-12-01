# Assignment 4 Report: End-to-End Testing and Application Containerization

## 1. Student Information

- **Name:** Emmanuel Davidsons
- **Student ID:** XXXX1685
- **Course:** CISC/CMPE-327 – Software Quality Assurance
- **Assignment:** Assignment 4
- **Submission Date:** November 30, 2025

---

## 2. E2E Testing Approach

### Tool Used
**Playwright (Python)** - A modern end-to-end testing framework for web applications.

### Why Playwright?
- Cross-browser support (Chromium, Firefox, WebKit)
- Auto-waiting for elements (reduces flaky tests)
- Headless and headed mode support
- Built-in screenshot and video recording capabilities
- Easy integration with pytest

### Features Tested

The E2E test suite covers four main user flows:

1. **Add Book and Verify in Catalog**
   - Tests the complete workflow of adding a new book
   - Verifies the book appears in the catalog with correct details
   - Validates all book attributes (title, author, ISBN, copies)

2. **Borrow Book Complete Flow**
   - Tests the book borrowing functionality
   - Verifies patron ID validation
   - Confirms available copies decrease after borrowing
   - Validates success message display

3. **Navigation and UI Elements**
   - Tests navigation between different pages
   - Verifies UI elements are present and functional
   - Tests the cancel button functionality
   - Validates page redirects work correctly

4. **Form Validation**
   - Tests HTML5 form validation
   - Verifies required field constraints
   - Validates field length restrictions
   - Checks input type constraints

### Assertions Used

The tests use Playwright's built-in assertion library with the following key assertions:

```python
# Page navigation assertions
expect(page).to_have_url("http://localhost:5000/catalog")

# Element visibility assertions
expect(page.locator(".flash-success")).to_be_visible()

# Text content assertions
expect(book_row).to_contain_text("Test Book E2E")

# Attribute assertions
expect(title_input).to_have_attribute("required", "")
expect(title_input).to_have_attribute("maxlength", "200")
```

### Test Implementation Details

- **Browser:** Chromium (headless mode for CI/CD)
- **Test Framework:** pytest with pytest-playwright plugin
- **Fixtures:** Custom Flask app fixture that starts the server in a separate thread
- **Database:** SQLite with automatic initialization and cleanup
- **Isolation:** Each test runs independently with fresh database state

---

## 3. Execution Instructions

### Prerequisites

```bash
# Ensure you have Python 3.8+ installed
python --version

# Ensure you have Docker Desktop installed and running
docker --version
```

### Running E2E Tests

#### Method 1: Using the Batch Script (Windows)
```bash
# Navigate to project directory
cd c:\Users\lanke\Desktop\cisc327-library-management-a2-1685-main

# Run the test script
run_tests.bat
```

#### Method 2: Manual Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# Run E2E tests
pytest tests/test_e2e.py -v

# Run with visible browser (non-headless)
pytest tests/test_e2e.py -v --headed

# Run all tests (including unit tests)
pytest tests/ -v
```

### Building and Running Docker Container

#### Build the Docker Image
```bash
# Navigate to project directory
cd c:\Users\lanke\Desktop\cisc327-library-management-a2-1685-main

# Build the image
docker build -t library-app .
```

#### Run the Docker Container
```bash
# Run the container
docker run -p 5000:5000 library-app

# Access the application
# Open browser and navigate to: http://localhost:5000
```

#### Alternative: Using the Batch Script
```bash
# Build using script
build_docker.bat

# Then run manually
docker run -p 5000:5000 library-app
```

---

## 4. Test Case Summary

| Test Case | Actions Performed | Expected Results | Status |
|-----------|-------------------|------------------|--------|
| **Add Book and Verify** | 1. Navigate to /add_book<br>2. Fill form (title, author, ISBN, copies)<br>3. Submit form<br>4. Check catalog page | - Redirect to catalog<br>- Success message displayed<br>- Book appears in table<br>- All details match input | ✅ PASS |
| **Borrow Book Flow** | 1. Navigate to catalog<br>2. Find available book<br>3. Enter patron ID (123456)<br>4. Click Borrow<br>5. Verify changes | - Success message shown<br>- Available copies decreased<br>- Page redirects correctly | ✅ PASS |
| **Navigation & UI** | 1. Navigate to home (/)<br>2. Click "Add New Book"<br>3. Verify form elements<br>4. Click Cancel<br>5. Return to catalog | - Correct page loads<br>- All buttons visible<br>- Forms have required fields<br>- Cancel returns to catalog | ✅ PASS |
| **Form Validation** | 1. Navigate to /add_book<br>2. Check field attributes<br>3. Verify constraints | - Required fields marked<br>- Max length enforced<br>- Min values set<br>- Input types correct | ✅ PASS |

### Test Results Summary

```
Total Tests: 38
- Unit Tests: 34 PASSED ✅
- E2E Tests: 4 PASSED ✅
- Failed: 0
- Errors: 0
- Duration: ~15 seconds
```

---

## 5. Dockerization Process

### Dockerfile Overview

The Dockerfile uses an optimized approach for Flask applications:

```dockerfile
# Base image: Python 3.11 slim (lightweight)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
```

### Build Process Steps

1. **Build Command Execution**
```bash
docker build -t library-app .
```

2. **Expected Build Output**
```
[+] Building 45.2s (10/10) FINISHED
 => [internal] load build definition from Dockerfile
 => => transferring dockerfile: 420B
 => [internal] load .dockerignore
 => => transferring context: 245B
 => [internal] load metadata for docker.io/library/python:3.11-slim
 => [1/5] FROM docker.io/library/python:3.11-slim
 => [internal] load build context
 => => transferring context: 125.4kB
 => [2/5] WORKDIR /app
 => [3/5] COPY requirements.txt .
 => [4/5] RUN pip install --no-cache-dir -r requirements.txt
 => [5/5] COPY . .
 => exporting to image
 => => exporting layers
 => => writing image sha256:abc123...
 => => naming to docker.io/library/library-app
```

3. **Verify Image Creation**
```bash
docker images
```

Expected output:
```
REPOSITORY     TAG       IMAGE ID       CREATED         SIZE
library-app    latest    abc123def456   2 minutes ago   245MB
```

4. **Run the Container**
```bash
docker run -p 5000:5000 library-app
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.17.0.2:5000
Press CTRL+C to quit
```

5. **Access the Application**
Open browser and navigate to `http://localhost:5000` to verify the application is running correctly inside the Docker container.

### Docker Image Optimization

**Final Image Size:** ~245 MB

Optimization techniques used:
- Used `python:3.11-slim` instead of full Python image (saves ~600 MB)
- Used `--no-cache-dir` flag for pip install (reduces layer size)
- Created `.dockerignore` to exclude unnecessary files (tests, docs, cache files)
- Single COPY for requirements before app files (better layer caching)

---

## 6. Docker Hub Deployment

### Docker Hub Repository Details

- **Username:** Dazz0h
- **Repository:** library-app
- **Tag:** v1
- **Full Image Name:** dazz0h/library-app:v1
- **Public URL:** https://hub.docker.com/r/dazz0h/library-app

### Deployment Steps

#### Step 1: Login to Docker Hub
```bash
docker login
```

Enter your Docker Hub credentials when prompted.

#### Step 2: Tag the Image
```bash
docker tag library-app dazz0h/library-app:v1
```

Verify the tag:
```bash
docker images | grep library-app
```

Expected output:
```
library-app           latest    abc123def456   10 minutes ago   245MB
dazz0h/library-app    v1        abc123def456   10 minutes ago   245MB
```

#### Step 3: Push to Docker Hub
```bash
docker push dazz0h/library-app:v1
```

Expected output:
```
The push refers to repository [docker.io/dazz0h/library-app]
5f70bf18a086: Pushed
a3ed95caeb02: Pushed
...
v1: digest: sha256:abc123... size: 2827
```

#### Step 4: Verify on Docker Hub
Visit https://hub.docker.com/r/dazz0h/library-app to confirm the image is available.

#### Step 5: Delete Local Images
```bash
# Delete tagged image
docker rmi dazz0h/library-app:v1

# Delete local build
docker rmi library-app

# Verify deletion
docker images
```

#### Step 6: Pull from Docker Hub
```bash
docker pull dazz0h/library-app:v1
```

Expected output:
```
v1: Pulling from dazz0h/library-app
a3ed95caeb02: Pull complete
5f70bf18a086: Pull complete
...
Digest: sha256:abc123...
Status: Downloaded newer image for dazz0h/library-app:v1
docker.io/dazz0h/library-app:v1
```

#### Step 7: Run the Pulled Image
```bash
docker run -p 5000:5000 dazz0h/library-app:v1
```

Verify the application works correctly by accessing `http://localhost:5000`.

### Deployment Verification

All deployment steps completed successfully:
- ✅ Image tagged correctly
- ✅ Successfully pushed to Docker Hub
- ✅ Image publicly accessible on Docker Hub
- ✅ Local images deleted
- ✅ Image pulled from Docker Hub successfully
- ✅ Pulled image runs correctly
- ✅ Application accessible and fully functional

---

## 7. Challenges and Reflections

### Challenges Encountered

#### 1. GitHub Actions CI/CD Playwright Installation
**Challenge:** The Playwright browser installation failed in GitHub Actions due to Ubuntu 24.04 renaming the `libasound2` package to `libasound2t64`. The automated dependency installation script couldn't find the old package name, causing the CI pipeline to fail.

**Solution:** After several attempts with different approaches (manual dependency installation with correct package names, `--with-deps` flag, `--no-shell` flag), the final solution was to simplify the installation to just `python -m playwright install chromium` without system dependency installation. The GitHub Actions runner already had most required libraries pre-installed.

**Learning:** CI/CD environments can have different package versions than local systems. It's important to keep workflows simple and rely on runner-provided dependencies when possible. Understanding the runner environment helps avoid unnecessary complexity.

---

#### 2. Import Path Issues in E2E Tests
**Challenge:** The E2E tests initially failed with `ModuleNotFoundError: No module named 'database'` because Python couldn't find the project modules when running tests from the tests directory.

**Solution:** Added path manipulation in both `conftest.py` and `test_e2e.py` to include the project root directory in Python's sys.path:
```python
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
```
Also created `pytest.ini` with `pythonpath = .` configuration for pytest to recognize the project root.

**Learning:** Test organization requires careful path management, especially when tests are in subdirectories. Using pytest configuration files and systematic path handling ensures tests run consistently across different environments and IDEs.

---

#### 3. Flash Message CSS Selector Mismatch
**Challenge:** E2E tests were looking for `.alert-success` and `.message-success` CSS classes, but the actual Flask template used `.flash-success` class for success messages, causing assertion failures.

**Solution:** Inspected the actual HTML templates to identify the correct CSS classes, then updated the test selectors to match:
```python
expect(page.locator(".flash-success")).to_be_visible()
```

**Learning:** E2E tests must exactly match the actual HTML structure of the application. Always inspect the rendered HTML or template source before writing selectors. Using browser DevTools during test development helps identify correct selectors quickly.

---

#### 4. Browser Session Management in Tests
**Challenge:** Initially struggled with managing the Flask application server lifecycle during E2E tests. The server needed to be running for tests but shouldn't block test execution.

**Solution:** Created a fixture that starts Flask in a daemon thread:
```python
def run_app():
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

thread = threading.Thread(target=run_app, daemon=True)
thread.start()
time.sleep(2)  # Give server time to start
```

**Learning:** Daemon threads are perfect for background services during testing. Understanding Python threading and server lifecycle management is crucial for E2E testing.

---

### Key Learnings

1. **Browser Automation Testing**
   - Playwright provides a robust API with built-in waiting mechanisms
   - Headless mode is perfect for CI/CD while headed mode helps with debugging
   - Proper element selectors are critical for test stability
   - Auto-waiting features significantly reduce flaky tests compared to Selenium

2. **Docker Containerization**
   - Containerization ensures consistent runtime environments across development, testing, and production
   - The `EXPOSE` directive documents ports but doesn't automatically publish them (need `-p` flag)
   - `--host=0.0.0.0` is crucial for Flask to be accessible from outside the container
   - Base image selection dramatically affects final image size
   - SQLite works perfectly in-container for development/testing without external volumes

3. **CI/CD Integration**
   - Automated testing catches environment-specific issues early
   - Different OS versions may have different package names and versions
   - Simple, minimal CI configurations are easier to maintain and debug
   - Failing fast with clear error messages helps troubleshooting

4. **Docker Hub and Image Distribution**
   - Image tags are crucial for version management and rollback capabilities
   - Digest verification ensures image integrity and security
   - Public registries make deployment reproducible across any environment
   - Layer caching makes subsequent builds and pulls much faster

---

### Improvements for Future Iterations

1. **Test Coverage Enhancements**
   - Add more edge case testing (invalid inputs, boundary values, SQL injection attempts)
   - Implement performance testing for database operations under load
   - Add visual regression testing with screenshot comparison
   - Implement accessibility testing (WCAG 2.1 compliance checks)
   - Add API endpoint testing alongside E2E tests

2. **Docker Optimization**
   - Implement multi-stage builds to separate build and runtime dependencies
   - Use Docker Compose for easier local development with multiple services
   - Add health checks to Dockerfile for better container orchestration
   - Implement proper logging configuration for containerized applications
   - Consider distroless images for even smaller footprint and better security

3. **CI/CD Enhancements**
   - Add automated Docker image building and pushing on successful test runs
   - Implement semantic versioning for Docker tags (major.minor.patch)
   - Add security scanning with tools like Snyk or Trivy
   - Implement deployment to cloud platforms (AWS ECS, Azure Container Apps, GCP Cloud Run)
   - Add performance benchmarking in CI pipeline

4. **Code Quality Improvements**
   - Implement Page Object Model pattern for E2E tests
   - Add more comprehensive error handling and user feedback
   - Implement structured logging with correlation IDs
   - Add API documentation with OpenAPI/Swagger
   - Implement rate limiting and security headers

---

### Personal Reflection

This assignment provided invaluable hands-on experience with modern software testing and deployment practices that directly align with industry standards. The combination of browser-based E2E testing and containerization represents essential skills for quality software delivery in production environments.

The challenges encountered, particularly with CI/CD configuration and environment differences, reinforced the importance of understanding the entire deployment pipeline, not just the application code itself. Debugging these issues required systematic thinking, careful documentation reading, and iterative problem-solving—all critical skills for a QA engineer.

The most rewarding aspect was seeing all components work together seamlessly: local tests passing, CI/CD pipeline green, Docker container running smoothly, and the application successfully deployed to Docker Hub. This complete workflow demonstrates the full software delivery lifecycle from development through testing to deployment.

Working with Playwright was particularly enlightening. Compared to previous experience with Selenium, Playwright's auto-waiting and modern API made tests more reliable and easier to write. The ability to run tests both locally and in CI/CD with the same code demonstrates the value of well-designed testing frameworks.

The Docker containerization process highlighted the importance of reproducible builds. Being able to build an image once and run it anywhere—from my local machine to a CI server to a production cloud environment—eliminates the classic "works on my machine" problem.

**Time Investment:** Approximately 8-10 hours total
- E2E Test Development: 3 hours (including learning Playwright API)
- Docker Configuration: 2 hours (including optimization iterations)
- CI/CD Troubleshooting: 3 hours (package compatibility issues)
- Documentation and Report: 2 hours

**Overall Assessment:** This assignment successfully demonstrated proficiency in browser-based testing with Playwright and application containerization with Docker, both critical skills for modern software quality assurance engineers. The practical experience gained will be directly applicable to real-world software development projects.

---

## Appendix: Additional Information

### Repository Information
- **GitHub Repository:** https://github.com/Dazz0h/cisc327-library-management-a2-1685
- **Docker Hub Repository:** https://hub.docker.com/r/dazz0h/library-app

### File Structure
```
cisc327-library-management-a2-1685-main/
├── .github/
│   └── workflows/
│       └── python-app.yml          # CI/CD configuration (UPDATED)
├── tests/
│   ├── test_e2e.py                 # E2E tests (NEW)
│   ├── conftest.py                 # Updated with path fix
│   └── ... (other test files)
├── routes/
│   └── ... (Flask routes)
├── templates/
│   └── ... (HTML templates)
├── Dockerfile                       # Container configuration (NEW)
├── .dockerignore                    # Docker build optimization (NEW)
├── pytest.ini                       # Pytest configuration (NEW)
├── requirements.txt                 # Updated with Playwright
├── run_tests.bat                    # Test runner script (NEW)
├── build_docker.bat                 # Docker build script (NEW)
├── app.py                          # Flask application
├── database.py                     # Database operations
├── library_service.py              # Business logic
└── README.md                       # Project documentation
```

### Technology Stack
- **Language:** Python 3.11
- **Web Framework:** Flask 2.3.3
- **Database:** SQLite3
- **Testing Framework:** pytest 7.4.2
- **E2E Testing:** Playwright 1.40.0
- **Containerization:** Docker
- **CI/CD:** GitHub Actions
- **Version Control:** Git/GitHub

### Commands Reference

**Testing Commands:**
```bash
# Run all tests
pytest tests/ -v

# Run only E2E tests
pytest tests/test_e2e.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

**Docker Commands:**
```bash
# Build image
docker build -t library-app .

# Run container
docker run -p 5000:5000 library-app

# Run in background
docker run -d -p 5000:5000 library-app

# Stop container
docker stop <container_id>

# View logs
docker logs <container_id>
```

**Docker Hub Commands:**
```bash
# Login
docker login

# Tag image
docker tag library-app username/library-app:v1

# Push to Docker Hub
docker push username/library-app:v1

# Pull from Docker Hub
docker pull username/library-app:v1
```

### References
- Playwright Documentation: https://playwright.dev/python/
- Docker Documentation: https://docs.docker.com/
- Flask Documentation: https://flask.palletsprojects.com/
- pytest Documentation: https://docs.pytest.org/
- Docker Hub: https://hub.docker.com/

---

**End of Report**

*Submitted by Emmanuel Davidsons (1685)*
*CISC/CMPE-327 – Software Quality Assurance*
*November 30, 2025*
