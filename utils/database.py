"""Database utility functions."""

from typing import Any, List, Optional, Dict
from sqlalchemy.orm import Session
from config.database import _SessionLocal


def get_session() -> Session:
    """Get database session.
    
    Returns:
        Database session
    """
    return _SessionLocal()


def execute_query(query: str, params: Dict[str, Any] = None) -> List[Any]:
    """Execute raw SQL query.
    
    Args:
        query: SQL query string
        params: Query parameters
        
    Returns:
        Query results
    """
    db = get_session()
    try:
        result = db.execute(query, params or {})
        return result.fetchall()
    finally:
        db.close()


def fetch_one(query: str, params: Dict[str, Any] = None) -> Optional[Any]:
    """Fetch single row from query.
    
    Args:
        query: SQL query string
        params: Query parameters
        
    Returns:
        Single row or None
    """
    db = get_session()
    try:
        result = db.execute(query, params or {})
        return result.fetchone()
    finally:
        db.close()


def fetch_all(query: str, params: Dict[str, Any] = None) -> List[Any]:
    """Fetch all rows from query.
    
    Args:
        query: SQL query string
        params: Query parameters
        
    Returns:
        List of rows
    """
    return execute_query(query, params)
