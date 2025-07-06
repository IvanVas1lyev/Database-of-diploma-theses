from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/thesis_db"
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Thesis Database API"
    
    # CORS
    backend_cors_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    
    # Python execution
    code_execution_timeout: int = 10
    max_code_length: int = 10000
    
    class Config:
        env_file = ".env"


settings = Settings()