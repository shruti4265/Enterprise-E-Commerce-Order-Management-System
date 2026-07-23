from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from database import Base


class Cart(Base):

    __tablename__ = "carts"

    cart_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False,
        unique=True
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    def __repr__(self):

        return (
            f"Cart("
            f"cart_id={self.cart_id}, "
            f"customer_id={self.customer_id}"
            f")"
        )