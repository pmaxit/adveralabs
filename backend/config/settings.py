"""Application settings and configuration."""
import os
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/marketing_db",
        alias="DATABASE_URL"
    )
    
    # LLM Configuration
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", alias="ANTHROPIC_API_KEY")
    llm_provider: Literal["openai", "anthropic"] = Field(
        default="openai",
        alias="LLM_PROVIDER"
    )
    
    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL"
    )
    
    # API Configuration
    api_secret_key: str = Field(
        default="your_secret_key_here",
        alias="API_SECRET_KEY"
    )
    api_algorithm: str = Field(default="HS256", alias="API_ALGORITHM")
    api_access_token_expire_minutes: int = Field(
        default=30,
        alias="API_ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    
    # External API Keys
    google_ads_api_key: str = Field(default="", alias="GOOGLE_ADS_API_KEY")
    facebook_ads_api_key: str = Field(default="", alias="FACEBOOK_ADS_API_KEY")
    google_analytics_api_key: str = Field(
        default="",
        alias="GOOGLE_ANALYTICS_API_KEY"
    )
    
    # Environment
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        alias="ENVIRONMENT"
    )
    
    # Feature Flags
    enable_agent_orchestration: bool = Field(default=True)
    enable_caching: bool = Field(default=True)
    enable_rate_limiting: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
