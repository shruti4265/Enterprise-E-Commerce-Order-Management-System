"""
logger.py
=========

Common logging module for the Enterprise E-Commerce Order Management System.

Every team member should import get_logger() from this file instead of
creating their own logging configuration.

Usage:
    from utilities.logger import get_logger

    logger = get_logger(__name__)

    logger.info("Customer added successfully.")
    logger.warning("Low stock for Product ID 12.")
    logger.error("Payment failed.", exc_info=True)
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

# ============================================================================
# Log Configuration
# ============================================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOG_DIR = os.path.join(BASE_DIR, "logs")

APP_LOG_FILE = os.path.join(LOG_DIR, "app.log")

ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

CONSOLE_LEVEL = logging.INFO

FILE_LEVEL = logging.INFO

ERROR_LEVEL = logging.ERROR

_configured_loggers = set()


# ============================================================================
# Create Logs Folder
# ============================================================================

def create_log_directory():
    """
    Creates the logs directory if it does not exist.
    """
    os.makedirs(LOG_DIR, exist_ok=True)


# ============================================================================
# Logger Function
# ============================================================================

def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a configured logger.

    Parameters
    ----------
    module_name : str
        Usually pass __name__.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(module_name)

    if module_name in _configured_loggers:
        return logger

    create_log_directory()

    logger.setLevel(logging.DEBUG)

    logger.propagate = False

    formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # -----------------------------------------------------------------------
    # Console Handler
    # -----------------------------------------------------------------------

    console_handler = logging.StreamHandler()

    console_handler.setLevel(CONSOLE_LEVEL)

    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # -----------------------------------------------------------------------
    # Application Log
    # -----------------------------------------------------------------------

    app_handler = TimedRotatingFileHandler(
        APP_LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=14,
        encoding="utf-8"
    )

    app_handler.setLevel(FILE_LEVEL)

    app_handler.setFormatter(formatter)

    logger.addHandler(app_handler)

    # -----------------------------------------------------------------------
    # Error Log
    # -----------------------------------------------------------------------

    error_handler = TimedRotatingFileHandler(
        ERROR_LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30,
        encoding="utf-8"
    )

    error_handler.setLevel(ERROR_LEVEL)

    error_handler.setFormatter(formatter)

    logger.addHandler(error_handler)

    _configured_loggers.add(module_name)

    return logger


# ============================================================================
# Test Logger
# ============================================================================

if __name__ == "__main__":

    logger = get_logger(__name__)

    logger.debug("Debug message.")

    logger.info("Logger initialized successfully.")

    logger.warning("This is a warning message.")

    try:
        result = 10 / 0

    except ZeroDivisionError:

        logger.error(
            "Division by zero occurred.",
            exc_info=True
        )

    print("\nLogger test completed successfully.")
    print(f"Log directory : {LOG_DIR}")
    print(f"Application Log : {APP_LOG_FILE}")
    print(f"Error Log : {ERROR_LOG_FILE}")