"""
File: models/product_model.py
Description: SQLAlchemy model for Product table.
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Product(Base):
    """
    Product Model
    """

    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)

    product_name = Column(String(150), nullable=False)

    product_description = Column(String(500))

    product_price = Column(Float, nullable=False)

    product_quantity = Column(Integer, nullable=False, default=0)

    product_status = Column(String(50), nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.category_id"),
        nullable=False
    )

    # Many Products -> One Category
    category_object = relationship(
        "Category",
        back_populates="product_list"
    )

    def __repr__(self):
        return (
            f"<Product("
            f"product_id={self.product_id}, "
            f"product_name='{self.product_name}', "
            f"product_price={self.product_price}, "
            f"product_quantity={self.product_quantity}, "
            f"product_status='{self.product_status}', "
            f"category_id={self.category_id})>"
        )