@echo off
echo Job Search Agent
echo ================

echo.
echo Choose an option:
echo 1. Run job search once
echo 2. Start scheduler (runs automatically)
echo 3. Run tests
echo 4. Setup (first time only)
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo Running job search once...
    python job_search_agent.py once
    pause
) else if "%choice%"=="2" (
    echo Starting scheduler...
    python job_search_agent.py
    pause
) else if "%choice%"=="3" (
    echo Running tests...
    python test_agent.py
    pause
) else if "%choice%"=="4" (
    echo Running setup...
    python setup.py
    pause
) else (
    echo Invalid choice. Please run the script again.
    pause
)
