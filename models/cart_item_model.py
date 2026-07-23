from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)

from database import Base


class CartItem(Base):

    __tablename__ = "cart_items"

    cart_item_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    cart_id = Column(
        Integer,
        ForeignKey("carts.cart_id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False,
        default=1
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    subtotal = Column(
        Float,
        nullable=False
    )

    def __repr__(self):

        return (
            f"CartItem("
            f"cart_item_id={self.cart_item_id}, "
            f"cart_id={self.cart_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"subtotal={self.subtotal}"
            f")"
        )