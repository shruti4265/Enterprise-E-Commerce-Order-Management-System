"""
Initialize database tables.

After all models are created, import them here
before calling init_db().
"""

from database import init_db

if __name__ == "__main__":
    init_db()