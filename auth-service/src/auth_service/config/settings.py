"""
Application configuration using Pydantic Settings.
Follows the 12-Factor methodology for configuration management.
"""

import secrets
from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, validator
from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):
    """Database configuration settings."""

    # Database URL - supports both SQLite and PostgreSQL
    url:str=Field(
        default="sqlite+aiosqlite:///.auth.db", description="Database URL",
    )

    # Connection pool settings
    pool_size:int=Field(
        default=10, description="Database connection pool size",
    )
    max_overflow:int=Field(
        default=20, description="Maximum overflow connections."
    )
    pool_timeout:int=Field(
        default=30, description="Pool timeout in seconds",
    )
    pool_recycle:int=Field(
        default=3600, description="Pool recycle time in seconds",
    )

    # Query settings
    echo:bool=Field(
        default=False, description="Echo SQL queries"
    )

    class Config:
        env_prefix="DB_"


class SecuritySettings(BaseSettings):
    """Security-related configuration."""

    # JWT configurations
    secret_key:str=Field(
        default_factory=lambda:secrets.token_urlsafe(32),
        description="Secret key for JWT token signing",
    )
    algorithm:str=Field(default="HS256", description="JWT signing algorithm")
    access_token_expire_minutes:int=Field(
        default=30, description="Refresh token expiration time in days",
    )

    # Password configuration
    password_min_length:int=Field(default=8, description="Minimum password length")
    password_max_length:int=Field(default=128, description="Maximum password length")
    password_require_uppercase:bool=Field(default=True, description="Require uppercase letters in password string")
    password_require_lowercase:bool=Field(default=True, description="Require lowercase letters in password string")
    password_require_numbers:bool=Field(default=True, description="Require numbers in password string")
    password_require_special:bool=Field(default=True, description="Require special characters in password string")

    # Rate limiting
    rate_limit_requests:int=Field(default=100, description="Number of requests allowed per window")
    rate_limit_window:int=Field(default=3600, description="Rate limit window in seconds")

    # Account security
    max_login_attempts:int=Field(default=5, description="Maximum allowed failed login attempts before account lockdown")
    lockdown_duration:int=Field(default=900, description="Account lockdown duration in seconds")

    @validator("secret_key")
    def validate_secret_key(cls, v:str):
        """Ensure secret key is sufficiently long."""
        if len(v)<32:
            raise ValueError("Secret key must be at least 32 characters long.")
        return v

    class Config:
        env_prefix="SECURITY_"


class EmailSettings(BaseSettings):
    """Email service configuration."""

    smtp_host:str=Field(default="localhost", description="SMTP server host")
    smtp_port:int=Field(default=587, description="SMTP server port")
    smtp_username:str=Field(default="", description="SMTP username")
    smtp_password:str=Field(default="", description="SMTP password")
    smtp_use_tls:bool=Field(default=True, description="Use TLS for SMTP")

    from_email:str=Field(default="noreply@email.com", description="Default from email address")
    from_name:str=Field(default="Auth Service", description="Default from name")

    # Email verification
    verification_token_expire_hours:int=Field(default=24, description="Email verification token expiration in hours")

    class Config:
        env_prefix="EMAIL_"


class AppSettings(BaseSettings):
    """Main application settings."""

    # Application metadata
    title:str=Field(default="Authentication Service", description="Application title")
    description:str=Field(default="Professional authentication microservice", description="Application description")
    version:str=Field(default="0.1.0", description="Application version")

    # Environment configuration
    environment:Literal["development", "testing", "production"]=Field(
        default="development",
        description="Application preferred environment",
    )

    # API configuration
    api_v1_prefix:str=Field(default="/api/v1", description="API v1 path prefix")
    docs_url:str | None=Field(default="/docs", description="OpenAPI docs URL")
    redoc_url:str | None=Field(default="/redoc", description="ReDoc URL")
    openapi_url:str | None=Field(default="/openapi.json", description="OpenAPI JSON URL")

    # Server configuration
    host:str=Field(default="127.0.0.1", description="Server host")
    port:int=Field(default=8000, description="Server port")
    reload:bool=Field(default=True, description="Auto-reload on code changes")

    # CORS configurations
    allowed_origins:list[str]=Field(
        default=["http://localhost:3000"],
        description="Allowed CORS origins",
    )
    allowed_methods:list[str]=Field(
        default=["GET", "POST", "PUT", "DELETE"],
        description="Allowed CORS methods",
    )
    allowed_headers:list[str]=Field(
        default=["*"],
        description="Allowed CORS headers",
    )

    # Logging configuration
    log_level:Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]=Field(
        default="INFO",
        description="Logging level",
    )
    log_format:Literal["json", "console"]=Field(
        default="console",
        description="Log format",
    )

    @validator("environment")
    def validate_environment(cls, v:str)->str:
        """Adjust settings based on environment."""
        return v.lower()

    @validator("docs_url", "redoc_url", "openai_url")
    def disable_docs_in_production(cls, v:str | None, values:dict)->str | None:
        """Disables API documentation in production."""
        if values.get("environment")=="production":
            return None
        return v

    class Config:
        env_prefix="APP_"
        case_sensitive=False


class Settings(BaseSettings):
    """Complete application settings."""

    app:AppSettings=Field(default_factory=AppSettings)
    database:DatabaseSettings=Field(default_factory=DatabaseSettings)
    security:SecuritySettings=Field(default_factory=SecuritySettings)
    email:EmailSettings=Field(default_factory=EmailSettings)

    class Config:
        env_file='.env'
        env_file_encoding="utf-8"
        env_nested_delimiter="__"


@lru_cache()
def get_settings()->Settings:
    """
    Get application settings instance.
    Uses lru_cache to ensure configurations are loaded only once.

    :return: Application settings instance.
    """
    return Settings()


# Convenience accessors
def get_app_settings()->AppSettings:
    """Get application settings."""
    return get_settings().app

def get_database_settings()->DatabaseSettings:
    """Get all database configurations."""
    return get_settings().database

def get_security_settings()->SecuritySettings:
    """Get security configurations."""
    return get_settings().security

def get_email_settings()->EmailSettings:
    """Get email settings."""
    return get_settings().email