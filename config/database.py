"""Database configuration and connection management."""

import os
from typing import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Database configuration class."""

    def __init__(self):
        """Initialize database configuration from environment variables."""
        self.host = os.getenv("DATABASE_HOST", "localhost")
        self.port = int(os.getenv("DATABASE_PORT", 5432))
        self.username = os.getenv("DATABASE_USER", "his_user")
        self.password = os.getenv("DATABASE_PASSWORD", "")
        self.database = os.getenv("DATABASE_NAME", "his_main")
        self.echo = os.getenv("DATABASE_ECHO", "False") == "True"

    @property
    def url(self) -> str:
        """Get database URL."""
        return (
            f"postgresql://{self.username}:{self.password}@"
            f"{self.host}:{self.port}/{self.database}"
        )

    def get_engine(self):
        """Create and return database engine."""
        engine = create_engine(
            self.url,
            echo=self.echo,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
        )

        # Enable foreign keys
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            if "sqlite" in self.url:
                cursor = dbapi_conn.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        return engine


# Global database configuration
_db_config = DatabaseConfig()
_engine = _db_config.get_engine()
_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_db_engine():
    """Get database engine."""
    return _engine


def get_db_session() -> Generator[Session, None, None]:
    """Get database session generator."""
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """Context manager for database session."""
    db = _SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
