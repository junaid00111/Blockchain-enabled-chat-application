@echo off
setlocal

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 goto error
)

set "PYTHON=venv\Scripts\python.exe"

echo Installing requirements...
"%PYTHON%" -m pip install -r requirements.txt
if errorlevel 1 goto error

echo Applying database migrations...
"%PYTHON%" manage.py migrate
if errorlevel 1 goto error

echo.
echo Starting Blockchain Chat...
echo Open this device: http://127.0.0.1:8000/
echo Other devices on same WiFi: http://YOUR-COMPUTER-IP:8000/
echo.
"%PYTHON%" manage.py runserver 0.0.0.0:8000
goto end

:error
echo.
echo Something went wrong while starting the project.
pause

:end
endlocal
