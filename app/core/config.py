from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    secret_key: str = "change-me"
    database_url: str = "sqlite:///./data/pocketsmart.db"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    access_token_expire_minutes: int = 1440
    frontend_origin: str = "http://127.0.0.1:8000"
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

settings = Settings()
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
DATA_DIR.mkdir(exist_ok=True)
UPLOAD_DIR.mkdir(exist_ok=True)
