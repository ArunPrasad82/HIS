"""Data validators."""

import re
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email address.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        return False, "Invalid email format"
    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """Validate phone number.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Indian phone number format
    phone_clean = re.sub(r"\D", "", phone)
    if len(phone_clean) != 10:
        return False, "Phone number must be 10 digits"
    if not phone_clean.startswith(("6", "7", "8", "9")):
        return False, "Invalid phone number"
    return True, None


def validate_aadhar(aadhar: str) -> Tuple[bool, Optional[str]]:
    """Validate Aadhar number.
    
    Args:
        aadhar: Aadhar number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    aadhar_clean = re.sub(r"\D", "", aadhar)
    if len(aadhar_clean) != 12:
        return False, "Aadhar number must be 12 digits"
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit"
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character"
    return True, None


def validate_pan(pan: str) -> Tuple[bool, Optional[str]]:
    """Validate PAN number.
    
    Args:
        pan: PAN number to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    pan_pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
    if not re.match(pan_pattern, pan.upper()):
        return False, "Invalid PAN format"
    return True, None
