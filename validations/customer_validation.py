import re

from sqlalchemy import select

from database import get_db_session
from models.customer_model import Customer


def validate_required_fields(*fields):
    """
    Returns True if every field is provided (not None and not empty).
    """
    return all(field not in (None, "") for field in fields)


def validate_email(email):
    """
    Returns True if the email string looks like a valid email address.
    """
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    Returns True if the phone string is all digits and a reasonable length.
    """
    return phone.isdigit() and 7 <= len(phone) <= 15


def check_duplicate_email(email):
    """
    Returns True if a customer with this email already exists in the database.
    """
    with get_db_session() as session:
        statement = select(Customer).where(Customer.email == email)
        existing = session.scalars(statement).first()
        return existing is not None