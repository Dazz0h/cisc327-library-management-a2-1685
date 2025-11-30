@echo off
echo ========================================
echo  Assignment 4 - Docker Build Script
echo ========================================
echo.

echo Building Docker image...
docker build -t library-app .
echo.

echo ========================================
echo  Build Complete!
echo ========================================
echo.
echo To run the container, use:
echo   docker run -p 5000:5000 library-app
echo.
echo Then open: http://localhost:5000
echo.
pause
