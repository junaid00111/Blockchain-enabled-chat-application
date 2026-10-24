$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

if (-not (Test-Path ".\venv\Scripts\python.exe")) {
    Write-Host "Creating virtual environment..."
    python -m venv venv
}

$python = ".\venv\Scripts\python.exe"

Write-Host "Installing requirements..."
& $python -m pip install -r requirements.txt

Write-Host "Applying database migrations..."
& $python manage.py migrate

Write-Host ""
Write-Host "Starting Blockchain Chat..."
Write-Host "Open this device: http://127.0.0.1:8000/"
Write-Host "Other devices on same WiFi: http://YOUR-COMPUTER-IP:8000/"
Write-Host ""

& $python manage.py runserver 0.0.0.0:8000
