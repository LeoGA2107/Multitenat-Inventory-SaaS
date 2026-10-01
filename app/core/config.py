from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # App Settings
    PROJECT_NAME: str = "SaaS Multitenant API"


    # Infraestructure connections
    DATABASE_URL: str = "postgresql+asyncpg://user:access@db:5432/saas_db"
    REDIS_URL: str = "redis://redis:6379/0"

    model_config = SettingsConfigDict(
        env_file= ".env", 
        env_file_encoding="utf-8", 
        extra="ignore")

    
    
# Singnle Global Settings Instance
settings = Settings()

