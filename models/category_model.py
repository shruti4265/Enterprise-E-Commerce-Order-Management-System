"""
File: models/category_model.py
Description: SQLAlchemy model for Category table.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    """
    Category Model
    """

    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(100), nullable=False, unique=True)

    # One Category -> Many Products
    product_list = relationship(
        "Product",
        back_populates="category_object",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Category("
            f"category_id={self.category_id}, "
            f"category_name='{self.category_name}')>"
        )