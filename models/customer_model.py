from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Customer(Base):

    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )

    addresses = relationship(
        "Address",
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    def __init__(self, customer_name, customer_email, customer_phone):

        self.name = customer_name
        self.email = customer_email
        self.phone = customer_phone
        self.is_active = True

    def __str__(self):

        return (
            f"Customer ID : {self.customer_id}\n"
            f"Name        : {self.name}\n"
            f"Email       : {self.email}\n"
            f"Phone       : {self.phone}\n"
            f"Status      : {'Active' if self.is_active else 'Inactive'}"
        )