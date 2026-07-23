from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.sql import func

from database import Base


class Order(Base):

    __tablename__ = "orders"

    order_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id"),
        nullable=False
    )

    order_date = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    total_amount = Column(
        Float,
        nullable=False
    )

    order_status = Column(
        String(30),
        nullable=False,
        default="Pending"
    )

    def __repr__(self):

        return (
            f"Order("
            f"order_id={self.order_id}, "
            f"customer_id={self.customer_id}, "
            f"total_amount={self.total_amount}, "
            f"status='{self.order_status}'"
            f")"
        )