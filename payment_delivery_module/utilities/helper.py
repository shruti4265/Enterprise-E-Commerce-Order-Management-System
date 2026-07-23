"""
helper.py
=========

Common helper functions for the Payment & Shipment module.
"""

from datetime import datetime
import random
import string


# ============================================================================
# Generate Tracking Number
# ============================================================================

def generate_tracking_number():
    """
    Generates a unique shipment tracking number.
    """

    prefix = "TRK"

    random_part = "".join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=10
        )
    )

    return f"{prefix}{random_part}"


# ============================================================================
# Generate Payment Reference
# ============================================================================

def generate_payment_reference():
    """
    Generates a unique payment reference number.
    """

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    random_digits = random.randint(1000, 9999)

    return f"PAY{timestamp}{random_digits}"


# ============================================================================
# Current Date & Time
# ============================================================================

def current_datetime():
    """
    Returns the current system date and time.
    """

    return datetime.now()


# ============================================================================
# Currency Formatter
# ============================================================================

def format_currency(amount):
    """
    Formats amount as currency.
    """

    return f"₹{amount:.2f}"


# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":

    print("Tracking Number :", generate_tracking_number())

    print("Payment Reference :", generate_payment_reference())

    print("Current Date & Time :", current_datetime())

    print("Formatted Amount :", format_currency(1250.75))