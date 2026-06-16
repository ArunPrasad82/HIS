"""Authentication utilities."""

import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config.settings import AppSettings


def hash_password(password: str) -> str:
    """Hash password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password
    """
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(password: str, hashed: str) -> bool:
    """Verify password against hash.
    
    Args:
        password: Plain text password
        hashed: Hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))


def create_token(user_id: int, user_data: Dict[str, Any]) -> str:
    """Create JWT token.
    
    Args:
        user_id: User ID
        user_data: User data dictionary
        
    Returns:
        JWT token
    """
    payload = {
        "user_id": user_id,
        "username": user_data.get("username"),
        "role": user_data.get("role"),
        "hospital_id": user_data.get("hospital_id"),
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(seconds=AppSettings.JWT_EXPIRY),
    }
    return jwt.encode(payload, AppSettings.SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify JWT token.
    
    Args:
        token: JWT token
        
    Returns:
        Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, AppSettings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
