"""
File: models/product_model.py
Description: SQLAlchemy model for Product table.
"""

from sqlalchemy import (
    Column, Integer, String, DECIMAL, Boolean,
    DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Product(Base):
    """
    Product Model
    """

    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    description = Column(Text)

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False
    )

    price = Column(DECIMAL(10, 2), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    # Many Products -> One Category
    category_object = relationship(
        "Category",
        back_populates="product_list"
    )

    def __repr__(self):
        return (
            f"<Product(product_id={self.product_id}, name='{self.name}', "
            f"price={self.price}, is_active={self.is_active}, "
            f"category_id={self.category_id})>"
        )