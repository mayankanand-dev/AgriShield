from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgriShield API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgrespassword@localhost:5432/agrishield_dev"
    
    # JWT Auth
    SECRET_KEY: str = "supersecretkey" # In production, read from env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # AI Mode
    AI_MODE: str = "mock" # mock | live
    MOCK_MODE: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
