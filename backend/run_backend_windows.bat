@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python launcher not found. Install Python 3.11+ first.
  pause
  exit /b 1
)
if not exist .venv py -3 -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
if not exist .env copy .env.example .env
 echo.
echo Backend starting on http://0.0.0.0:8000
 echo Open API docs at http://127.0.0.1:8000/docs
 echo Set NASA_EARTHDATA_USERNAME and NASA_EARTHDATA_PASSWORD in backend\.env before AppEEARS sampling.
uvicorn main:app --host 0.0.0.0 --port 8000
pause
