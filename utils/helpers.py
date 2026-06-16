"""Helper functions."""

from datetime import datetime, date
from typing import Optional, Union
import calendar


def format_date(date_obj: Union[date, datetime], format_str: str = "%d-%m-%Y") -> str:
    """Format date object to string.
    
    Args:
        date_obj: Date or datetime object
        format_str: Format string (default: DD-MM-YYYY)
        
    Returns:
        Formatted date string
    """
    if isinstance(date_obj, datetime):
        return date_obj.strftime(format_str)
    elif isinstance(date_obj, date):
        return date_obj.strftime(format_str)
    return str(date_obj)


def format_currency(amount: float, currency: str = "INR") -> str:
    """Format amount as currency.
    
    Args:
        amount: Amount to format
        currency: Currency code (default: INR)
        
    Returns:
        Formatted currency string
    """
    if currency == "INR":
        symbol = "₹"
    elif currency == "USD":
        symbol = "$"
    elif currency == "EUR":
        symbol = "€"
    else:
        symbol = currency
    
    return f"{symbol} {amount:,.2f}"


def get_age_from_dob(dob: Union[date, datetime]) -> int:
    """Calculate age from date of birth.
    
    Args:
        dob: Date of birth
        
    Returns:
        Age in years
    """
    if isinstance(dob, datetime):
        dob = dob.date()
    
    today = date.today()
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    return age


def get_age_details(dob: Union[date, datetime]) -> dict:
    """Get detailed age information.
    
    Args:
        dob: Date of birth
        
    Returns:
        Dictionary with years, months, days
    """
    if isinstance(dob, datetime):
        dob = dob.date()
    
    today = date.today()
    years = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    # Calculate months
    if today.month >= dob.month:
        months = today.month - dob.month
    else:
        months = 12 + today.month - dob.month
        years -= 1
    
    # Calculate days
    if today.day >= dob.day:
        days = today.day - dob.day
    else:
        days = calendar.monthrange(today.year, today.month - 1)[1] + today.day - dob.day
        months -= 1
    
    return {"years": max(0, years), "months": max(0, months), "days": max(0, days)}


def parse_date(date_str: str, format_str: str = "%d-%m-%Y") -> Optional[date]:
    """Parse date string to date object.
    
    Args:
        date_str: Date string
        format_str: Format string (default: DD-MM-YYYY)
        
    Returns:
        Date object or None if parsing fails
    """
    try:
        return datetime.strptime(date_str, format_str).date()
    except ValueError:
        return None


def get_first_day_of_month(date_obj: Union[date, datetime] = None) -> date:
    """Get first day of month.
    
    Args:
        date_obj: Date object (default: today)
        
    Returns:
        First day of month
    """
    if date_obj is None:
        date_obj = date.today()
    elif isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    return date_obj.replace(day=1)


def get_last_day_of_month(date_obj: Union[date, datetime] = None) -> date:
    """Get last day of month.
    
    Args:
        date_obj: Date object (default: today)
        
    Returns:
        Last day of month
    """
    if date_obj is None:
        date_obj = date.today()
    elif isinstance(date_obj, datetime):
        date_obj = date_obj.date()
    
    last_day = calendar.monthrange(date_obj.year, date_obj.month)[1]
    return date_obj.replace(day=last_day)


def truncate_text(text: str, length: int = 50, suffix: str = "...") -> str:
    """Truncate text to specified length.
    
    Args:
        text: Text to truncate
        length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated text
    """
    if len(text) > length:
        return text[: length - len(suffix)] + suffix
    return text


def capitalize_words(text: str) -> str:
    """Capitalize first letter of each word.
    
    Args:
        text: Text to capitalize
        
    Returns:
        Capitalized text
    """
    return " ".join(word.capitalize() for word in text.split())
