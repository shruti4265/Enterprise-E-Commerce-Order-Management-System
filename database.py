"""
database.py
===========

Common SQLAlchemy database module for the Enterprise E-Commerce
Order Management System.

Every team member should import from this file instead of creating
their own database connection.

Examples
--------

Model:

    from database import Base
    from sqlalchemy import Column, Integer, String

    class Customer(Base):
        __tablename__ = "customers"

        customer_id = Column(Integer, primary_key=True)
        customer_name = Column(String(100))

Database Session:

    from database import get_db_session

    with get_db_session() as session:
        session.add(customer)

Initialize Database:

    from database import init_db

    init_db()
"""

import os
from contextlib import contextmanager

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from utilities.logger import get_logger

# ============================================================================
# Logger
# ============================================================================

logger = get_logger(__name__)

# ============================================================================
# Database Configuration
# ============================================================================

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///enterprise_ecommerce.db"
)

CONNECT_ARGS = (
    {"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

engine = create_engine(
    DATABASE_URL,
    connect_args=CONNECT_ARGS,
    echo=False,
    future=True
)

# ============================================================================
# Enable SQLite Foreign Keys
# ============================================================================

if DATABASE_URL.startswith("sqlite"):

    @event.listens_for(Engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

# ============================================================================
# Session Factory
# ============================================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True
)

# ============================================================================
# Declarative Base
# ============================================================================

Base = declarative_base()

# ============================================================================
# Database Session
# ============================================================================


@contextmanager
def get_db_session():
    """
    Returns a database session.

    Automatically commits on success,
    rolls back on failure,
    and always closes the session.
    """

    session = SessionLocal()

    try:
        yield session

        session.commit()

    except SQLAlchemyError:

        session.rollback()

        logger.error(
            "Database transaction failed.",
            exc_info=True
        )

        raise

    except Exception:

        session.rollback()

        logger.error(
            "Unexpected database error.",
            exc_info=True
        )

        raise

    finally:

        session.close()

# ============================================================================
# Database Engine
# ============================================================================


def get_engine():
    """
    Returns the shared SQLAlchemy engine.
    """
    return engine

# ============================================================================
# Initialize Database
# ============================================================================


def init_db():
    """
    Creates all tables that are registered with Base.

    NOTE:
    Import every model before calling this function.
    """

    try:

        Base.metadata.create_all(bind=engine)

        logger.info(
            "Database initialized successfully."
        )

    except SQLAlchemyError:

        logger.error(
            "Failed to initialize database.",
            exc_info=True
        )

        raise

# ============================================================================
# Drop Database
# ============================================================================


def drop_all_tables():
    """
    Drops every table from the database.

    Use only during development/testing.
    """

    try:

        Base.metadata.drop_all(bind=engine)

        logger.warning(
            "All database tables dropped."
        )

    except SQLAlchemyError:

        logger.error(
            "Failed to drop database tables.",
            exc_info=True
        )

        raise

# ============================================================================
# Test
# ============================================================================

if __name__ == "__main__":

    logger.info("Testing database module...")

    init_db()

    with get_db_session() as session:

        logger.info(
            "Database session created successfully."
        )

        logger.info(
            "Session Active : %s",
            session.is_active
        )

    print("\nDatabase module executed successfully.")
    print(f"Database URL : {DATABASE_URL}")
    print(f"Engine : {engine}")