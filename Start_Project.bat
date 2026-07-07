@echo off
:: =========================================
:: Smart Crop Recommendation Project Launcher
:: =========================================

echo Starting the Smart Crop Recommendation Dashboard...

:: Step 1: Change to the directory where this batch file is located
:: This ensures the launcher works when the project folder is moved to another location
cd /d "%~dp0"
echo Changed directory to project root: %cd%

:: Step 2: Detect and activate the project's virtual environment
:: Checks standard naming conventions for Python virtual environments
if exist ".venv\Scripts\activate.bat" (
    echo Virtual environment '.venv' found. Activating...
    call ".venv\Scripts\activate.bat"
) else if exist "venv\Scripts\activate.bat" (
    echo Virtual environment 'venv' found. Activating...
    call "venv\Scripts\activate.bat"
) else (
    echo =======================================================
    echo ERROR: Virtual environment not found!
    echo Could not find '.venv' or 'venv' in the project folder.
    echo Please edit Start_Project.bat with the correct path
    echo to your virtual environment, or create one using:
    echo python -m venv venv
    echo =======================================================
    pause
    exit /b
)

:: Step 3: Verify Python is available
:: Confirms the python executable is available in the activated environment
echo Verifying Python installation...
python --version
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python is not recognized in the active virtual environment.
    pause
    exit /b
)

:: Step 4: Verify Streamlit is installed
:: Checks if the streamlit module is accessible through the python interpreter
python -c "import streamlit" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Streamlit is not installed in the active virtual environment.
    echo Please install dependencies using: pip install -r requirements.txt
    pause
    exit /b
)

:: Step 5: Launch Streamlit application using the active Python interpreter
:: This fixes the "'streamlit' is not recognized" issue by explicitly calling it via Python
echo Launching Streamlit application...
python -m streamlit run app.py

:: Step 6: Keep the terminal open with pause
:: Allows the user to read logs or errors after shutting down the server
pause
