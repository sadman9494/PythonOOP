@echo off
REM =====================================================
REM INFORMED SEARCH ALGORITHMS VISUALIZER
REM Complete Setup & Running Instructions (Windows)
REM =====================================================

echo.
echo 0x1f50d Informed Search Algorithms Visualizer
echo ========================================
echo.

REM Check Python Installation
echo Checking Python installation...
python --version

if errorlevel 1 (
    echo.
    echo ERROR: Python not found. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo.
echo ^/ Python is installed
echo.

REM Create Virtual Environment
echo Creating virtual environment...
python -m venv venv

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo ^/ Virtual environment created
echo.

REM Activate Virtual Environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo ^/ Virtual environment activated
echo.

REM Install Dependencies
echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo ^/ Dependencies installed
echo.

REM Run Application
echo Starting Streamlit application...
echo.
echo [INFO] The application will open in your browser automatically
echo [INFO] If not, visit: http://localhost:8501
echo.
echo [INFO] Press Ctrl+C to stop the server
echo.

streamlit run main.py

pause
