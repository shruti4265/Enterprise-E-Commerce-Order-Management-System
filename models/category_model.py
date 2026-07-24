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
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))

    # One Category -> Many Products
    product_list = relationship(
        "Product",
        back_populates="category_object"
    )

    def __repr__(self):
        return f"<Category(category_id={self.category_id}, name='{self.name}')>"