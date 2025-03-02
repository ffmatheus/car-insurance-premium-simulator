from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    AGE_RATE_PER_YEAR: float = 0.005
    VALUE_RATE_PER_10000: float = 0.005
    VALUE_BRACKET: float = 10000.0
    DEFAULT_COVERAGE_PERCENTAGE: float = 1.0

    ENABLE_GIS_ADJUSTMENT: bool = False
    MAX_GIS_ADJUSTMENT: float = 0.02
    MIN_GIS_ADJUSTMENT: float = -0.02

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    API_KEY: str = "698dc19d489c4e4db73e28a713eab07b"

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/car_insurance"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10

    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
