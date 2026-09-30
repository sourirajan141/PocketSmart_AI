# PocketSmart AI

GenAI-powered budget and recommendation assistant for Home Interior, Party Planning, and Jewelry.

## Features
- FastAPI backend with modular routes/services/models
- JWT authentication with SQLite persistence
- Home, Party and Jewelry planners
- Optional Gemini integration for AI recommendations
- Jewelry image upload support
- Safe fallback recommendations when Gemini is unavailable
- Responsive HTML/CSS/JavaScript frontend
- Recommendation history and session endpoints

## Quick start
Windows CMD:
```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python -m uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000

PowerShell activation alternative:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

If you do not add GEMINI_API_KEY, the application uses deterministic local fallback recommendations, so the UI and API remain testable.
