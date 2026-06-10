"""
Application configuration.

Demonstrates: OOP (Classes), Inheritance, Encapsulation, Abstraction
"""

import os
from datetime import timedelta
from abc import ABC, abstractmethod


class BaseConfig(ABC):
    """
    Abstract base configuration.
    Demonstrates: Abstraction, Encapsulation
    """

    # Encapsulated secret — never exposed directly
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod-2024")
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "jwt-secret-change-in-prod")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB upload limit

    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"}

    # Mail settings (optional)
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")

    @property
    @abstractmethod
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Subclasses must define the database URI."""

    @staticmethod
    def init_app(app) -> None:
        """Hook for app-level initialisation."""
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


class DevelopmentConfig(BaseConfig):
    """
    Development configuration — SQLite for zero-dependency local dev.
    Demonstrates: Inheritance
    """

    DEBUG = True
    TESTING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # type: ignore[override]
        # Use CMS_DATABASE_URL environment variable for database configuration
        return os.environ.get(
            "CMS_DATABASE_URL",
            "sqlite:///" + os.path.join(os.path.dirname(__file__), "..", "complaints_dev.db"),
        )


class ProductionConfig(BaseConfig):
    """
    Production configuration — MySQL via environment variable.
    Demonstrates: Inheritance, Polymorphism (overrides SQLALCHEMY_DATABASE_URI)
    """

    DEBUG = False
    TESTING = False

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # type: ignore[override]
        # CMS_DATABASE_URL takes precedence; falls back to SQLite
        uri = os.environ.get("CMS_DATABASE_URL")
        if not uri:
            return "sqlite:///" + os.path.join(os.path.dirname(__file__), "..", "complaints_prod.db")
        return uri


class TestingConfig(BaseConfig):
    """Testing configuration — in-memory SQLite."""

    TESTING = True
    DEBUG = True

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # type: ignore[override]
        return "sqlite:///:memory:"


# Registry of config objects — polymorphic dispatch by name
config_registry: dict[str, type[BaseConfig]] = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
