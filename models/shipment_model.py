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

    address_id = Column(
        Integer,
        ForeignKey("addresses.address_id"),
        nullable=False
    )

    shipment_status = Column(
        String(30),
        nullable=False,
        default="PROCESSING"
    )

    tracking_number = Column(
        String(50),
        nullable=True
    )

    shipped_date = Column(
        DateTime,
        nullable=True,
        server_default=func.now()
    )

    delivered_date = Column(
        DateTime,
        nullable=True
    )

    def __repr__(self):
        return (
            f"Shipment("
            f"shipment_id={self.shipment_id}, "
            f"order_id={self.order_id}, "
            f"address_id={self.address_id}, "
            f"shipment_status='{self.shipment_status}', "
            f"tracking_number='{self.tracking_number}'"
            f")"
        )