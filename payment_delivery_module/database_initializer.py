"""
Initialize database tables.

Import all models before calling init_db()
so SQLAlchemy registers them with Base.
"""

from database import init_db

# Import models
from models.payment_model import Payment
from models.shipment_model import Shipment


if __name__ == "__main__":
    init_db()