from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class Inventory(Base):

    __tablename__ = "inventory"

    inventory_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False,
        unique=True
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=0
    )

    low_stock_threshold = Column(
        Integer,
        nullable=False,
        default=10
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self):

        return (
            f"Inventory("
            f"inventory_id={self.inventory_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"low_stock_threshold={self.low_stock_threshold}"
            f")"
        )