from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgriShield API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres.lkwhqaiqzdutsxgeggko:AgriShield%40svh1@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"
    
    # JWT Auth
    SECRET_KEY: str = "supersecretkey" # In production, read from env
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # AI Mode
    AI_MODE: str = "mock" # mock | live
    MOCK_MODE: bool = True
    
    # Blockchain
    POLYGON_RPC_URL: str = "https://polygon-amoy.g.alchemy.com/v2/alch_Agu4ZKjaz7YRPE2ELTzIK"
    POLYGON_PRIVATE_KEY: str = "40b5ad267a0986e3336dd511e0feb85bd73acb2eab1163c93c25d840970629c4"
    SMART_CONTRACT_ADDRESS: str = "0x479c319C22928FF293713e70F24d399220d46876"
    
    model_config = {"env_file": ".env"}

settings = Settings()
