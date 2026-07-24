"""
database.py
===========

Common SQLAlchemy database module for the Enterprise
E-Commerce Order Management System.

Every team member must import Base and get_db_session()
from this file instead of creating their own database connection.

Example:

    from database import Base
    from database import get_db_session

    class Customer(Base):
        __tablename__ = "customers"

Later, after all model files are created, call:

    init_db()

to create all tables.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from utilities.logger import get_logger

# =============================================================================
# Logger
# =============================================================================

logger = get_logger(__name__)

# =============================================================================
# Database Configuration (MySQL)
# =============================================================================

DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username="root",
    password="Shruti",     # Change this on your own system
    host="localhost",
    port=3306,
    database="ecommerce_oms"
)

# =============================================================================
# Engine
# =============================================================================

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

# =============================================================================
# Session Factory
# =============================================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
    future=True
)

# =============================================================================
# Base Class
# =============================================================================

Base = declarative_base()

# =============================================================================
# Database Session
# =============================================================================


@contextmanager
def get_db_session():
    """
    Creates a database session.

    Automatically:
    - Commits on success
    - Rolls back on failure
    - Closes the session
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


# =============================================================================
# Get Engine
# =============================================================================

def get_engine():
    """
    Returns the shared SQLAlchemy engine.
    """

    return engine


# =============================================================================
# Initialize Database
# =============================================================================

def init_db():
    """
    Creates every table registered with SQLAlchemy Base.

    NOTE:
    Import all model files before calling this function.
    """

    try:

        Base.metadata.create_all(bind=engine)

        logger.info("Database initialized successfully.")

    except SQLAlchemyError:

        logger.error(
            "Failed to initialize database.",
            exc_info=True
        )

        raise


# =============================================================================
# Drop Database Tables
# =============================================================================

def drop_all_tables():
    """
    Drops all tables.

    Use only during development/testing.
    """

    try:

        Base.metadata.drop_all(bind=engine)

        logger.warning("All database tables dropped.")

    except SQLAlchemyError:

        logger.error(
            "Failed to drop database tables.",
            exc_info=True
        )

        raise


# =============================================================================
# Test Database Connection
# =============================================================================

if __name__ == "__main__":

    logger.info("Testing database connection...")

    try:

        with engine.connect() as connection:

            logger.info("MySQL connection established successfully.")

            print("\nConnected Successfully!")
            print(f"Database : {DATABASE_URL.database}")
            print(f"Host     : {DATABASE_URL.host}")
            print(f"Port     : {DATABASE_URL.port}")

    except Exception:

        logger.error(
            "Unable to connect to MySQL.",
            exc_info=True
        )

        print("Database connection failed.")