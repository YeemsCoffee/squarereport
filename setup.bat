@echo off
REM Setup script for Square Cafe Report application (Windows)

echo Setting up Square Cafe Report application...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create config file if it doesn't exist
if not exist config.yaml (
    echo Creating config.yaml from template...
    copy config.example.yaml config.yaml
    echo WARNING: Please edit config.yaml with your Square API credentials
)

echo.
echo Setup complete!
echo.
echo Next steps:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Edit config.yaml with your Square credentials
echo 3. Run the app: streamlit run app.py
echo.
pause
