import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App Config
    APP_NAME: str = "MusicApp Backend"
    DEBUG: bool = True
    
    # Firebase
    # Path to serviceAccountKey.json. If None, uses default credentials (mostly for production/GCP)
    FIREBASE_CREDENTIALS_PATH: str | None = None 
    FIREBASE_PROJECT_ID: str | None = None
    FIREBASE_STORAGE_BUCKET: str | None = None
    
    # Redis (Railway compatible)
    REDIS_URL: str = ""  # Set via Railway Redis plugin or local: redis://localhost:6379

    class Config:
        env_file = ".env"

settings = Settings()
