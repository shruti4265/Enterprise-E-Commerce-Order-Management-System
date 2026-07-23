from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from database import Base


class Shipment(Base):

    __tablename__ = "shipments"

    shipment_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    order_id = Column(
        Integer,
        ForeignKey("orders.order_id"),
        nullable=False
    )

    tracking_number = Column(
        String(100),
        nullable=False,
        unique=True
    )

    courier_name = Column(
        String(100),
        nullable=False
    )

    shipment_status = Column(
        String(30),
        nullable=False,
        default="Pending"
    )

    shipped_date = Column(
        DateTime,
        nullable=False,
        server_default=func.now()
    )

    def __repr__(self):

        return (
            f"Shipment("
            f"shipment_id={self.shipment_id}, "
            f"order_id={self.order_id}, "
            f"tracking_number='{self.tracking_number}', "
            f"courier_name='{self.courier_name}', "
            f"shipment_status='{self.shipment_status}'"
            f")"
        )