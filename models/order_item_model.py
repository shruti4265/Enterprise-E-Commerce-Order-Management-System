from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)

from database import Base


class OrderItem(Base):

    __tablename__ = "order_items"

    order_item_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    product_id = Column(
        Integer,
        ForeignKey("products.product_id"),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
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
            f"OrderItem("
            f"order_item_id={self.order_item_id}, "
            f"order_id={self.order_id}, "
            f"product_id={self.product_id}, "
            f"quantity={self.quantity}, "
            f"subtotal={self.subtotal}"
            f")"
        )