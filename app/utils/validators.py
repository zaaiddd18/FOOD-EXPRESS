"""
Validation utilities
"""
import re
from app.utils.errors import ValidationError


def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError('Invalid email format')
    return True


def validate_phone(phone):
    """Validate phone number format."""
    if phone and not re.match(r'^\+?[\d\s-]{10,}$', phone):
        raise ValidationError('Invalid phone number format')
    return True


def validate_required(data, fields):
    """Validate required fields."""
    missing = [field for field in fields if field not in data or not data[field]]
    if missing:
        raise ValidationError(f'Missing required fields: {", ".join(missing)}')
    return True


def validate_positive_number(value, field_name):
    """Validate positive number."""
    try:
        num = float(value)
        if num <= 0:
            raise ValidationError(f'{field_name} must be a positive number')
        return num
    except (ValueError, TypeError):
        raise ValidationError(f'{field_name} must be a valid number')

