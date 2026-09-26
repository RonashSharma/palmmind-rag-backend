from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    gemini_api_key: str
    redis_url: str
    redis_token: str
    database_url: str = "sqlite:///./palmmind.db"
    qdrant_path: str = "./qdrant_storage"

    class Config:
        env_file = ".env"

settings = Settings()