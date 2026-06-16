"""Application settings configuration."""

import os
from dotenv import load_dotenv

load_dotenv()


class AppSettings:
    """Application settings."""

    # App configuration
    APP_NAME = os.getenv("APP_NAME", "Hospital Information System")
    APP_ENV = os.getenv("APP_ENV", "development")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    VERSION = "1.0.0"

    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    JWT_EXPIRY = int(os.getenv("JWT_EXPIRY", 3600))  # 1 hour
    PASSWORD_MIN_LENGTH = 8

    # File upload
    MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10485760))  # 10MB
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "./logs/his.log")

    # Streamlit configuration
    STREAMLIT_THEME = "light"
    STREAMLIT_LAYOUT = "wide"

    # Pagination
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100

    # ABHA Configuration
    ABHA_ENABLED = os.getenv("ABHA_ENABLED", "True") == "True"
    ABHA_API_ENDPOINT = os.getenv("ABHA_API_ENDPOINT", "https://abha-api.ndhm.gov.in")

    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production environment."""
        return cls.APP_ENV == "production"

    @classmethod
    def is_development(cls) -> bool:
        """Check if running in development environment."""
        return cls.APP_ENV == "development"
