from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    AGE_RATE_PER_YEAR: float = Field(default=0.005)
    VALUE_RATE_PER_10000: float = Field(default=0.005)
    VALUE_BRACKET: float = Field(default=10000.0)
    DEFAULT_COVERAGE_PERCENTAGE: float = Field(default=1.0)

    ENABLE_GIS_ADJUSTMENT: bool = Field(default=False)
    MAX_GIS_ADJUSTMENT: float = Field(default=0.02)
    MIN_GIS_ADJUSTMENT: float = Field(default=-0.02)

    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
