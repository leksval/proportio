"""
Configuration management using Pydantic Settings.
Handles environment variables with validation and defaults.
"""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Server configuration
    server_name: str = Field(
        default="0.0.0.0",
        description="Server bind address"
    )
    
    server_port: int = Field(
        default=7860,
        ge=1024,
        le=65535,
        description="Server port (1024-65535)"
    )
    
    # Security configuration
    mcp_token: Optional[str] = Field(
        default=None,
        description="MCP authentication token (required for production)"
    )
    
    # Request limits
    max_request_size: int = Field(
        default=65536,  # 64KB
        ge=1024,
        le=1048576,  # 1MB max
        description="Maximum request body size in bytes"
    )
    
    # Development settings
    debug: bool = Field(
        default=False,
        description="Enable debug mode"
    )
    
    reload: bool = Field(
        default=False,
        description="Enable hot reload in development"
    )
    
    # Logging configuration
    log_level: str = Field(
        default="INFO",
        description="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    )
    
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug and self.mcp_token is not None
    
    def validate_production_settings(self) -> None:
        """Validate settings for production deployment."""
        if self.is_production():
            assert self.mcp_token, "MCP_TOKEN environment variable is required for production deployment"


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the current settings instance."""
    return settings


def setup_logging() -> None:
    """Configure logging based on settings."""
    import logging
    
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Set Gradio logging level
    if not settings.debug:
        logging.getLogger("gradio").setLevel(logging.WARNING)
        logging.getLogger("uvicorn").setLevel(logging.WARNING)


# Environment detection helpers
def is_huggingface_space() -> bool:
    """Check if running on Hugging Face Spaces."""
    return "SPACE_ID" in os.environ


def is_docker() -> bool:
    """Check if running in Docker container."""
    return os.path.exists("/.dockerenv") or "DOCKER_CONTAINER" in os.environ


def get_deployment_info() -> dict[str, str]:
    """Get deployment environment information."""
    info = {
        "environment": "unknown",
        "platform": "local"
    }
    
    if is_huggingface_space():
        info["platform"] = "huggingface_spaces"
        info["environment"] = "production"
    elif is_docker():
        info["platform"] = "docker"
        info["environment"] = "production" if settings.is_production() else "development"
    else:
        info["platform"] = "local"
        info["environment"] = "development"
    
    return info