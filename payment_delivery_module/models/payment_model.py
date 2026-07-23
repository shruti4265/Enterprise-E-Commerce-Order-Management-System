from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class Payment(Base):

    __tablename__ = "payments"

    payment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    amount = Column(
        Float,
        nullable=False
    )

    payment_method = Column(
        String(50),
        nullable=False
    )

    payment_status = Column(
        String(30),
        nullable=False,
        default="Pending"
    )

    payment_date = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    def __repr__(self):

        return (
            f"Payment("
            f"payment_id={self.payment_id}, "
            f"order_id={self.order_id}, "
            f"amount={self.amount}, "
            f"payment_method='{self.payment_method}', "
            f"payment_status='{self.payment_status}'"
            f")"
        )