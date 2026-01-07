"""
Application settings using Pydantic Settings.
"""

from functools import lru_cache
from typing import List, Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # === Application ===
    app_env: Literal["development", "staging", "production"] = "development"
    app_debug: bool = True
    app_secret_key: str = Field(..., min_length=32)

    # === Database ===
    database_url: str = Field(
        default="postgresql+asyncpg://medadreview:password@localhost:5432/medadreview_dev"
    )
    database_pool_size: int = 20
    database_max_overflow: int = 10

    # === Redis ===
    redis_url: str = "redis://localhost:6379/0"

    # === CLOVA OCR ===
    clova_ocr_api_url: str = ""
    clova_ocr_secret_key: str = ""

    # === Pinecone ===
    pinecone_api_key: str = ""
    pinecone_environment: str = "us-east-1"
    pinecone_index_name: str = "medadreview-legal-kb"

    # === LLM ===
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    llm_model: str = "claude-sonnet-4-20250514"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 8000

    # === Agent ===
    agent_max_iterations: int = 3
    agent_confidence_threshold: float = 0.8
    agent_auto_approve_threshold: float = 0.95

    # === JWT ===
    jwt_secret_key: str = Field(..., min_length=32)
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 480
    jwt_refresh_token_expire_days: int = 7

    # === S3/MinIO ===
    s3_endpoint_url: str = "http://localhost:9000"
    s3_access_key: str = "minioadmin"
    s3_secret_key: str = "minioadmin"
    s3_bucket_name: str = "medadreview-images"
    s3_region: str = "us-east-1"

    # === External APIs ===
    legal_api_base_url: str = "https://www.law.go.kr/api"

    # === Monitoring ===
    sentry_dsn: str = ""
    log_level: str = "INFO"

    # === CORS ===
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            import json

            return json.loads(v)
        return v

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
