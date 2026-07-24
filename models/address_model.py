from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Address(Base):

    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, autoincrement=True)

    customer_id = Column(
        Integer,
        ForeignKey("customers.customer_id", ondelete="CASCADE"),
        nullable=False
    )

    address_line1 = Column(String(150), nullable=False)
    address_line2 = Column(String(150))
    city = Column(String(80), nullable=False)
    state = Column(String(80), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(80), nullable=False)
    is_default = Column(Boolean, default=False)

    customer = relationship(
        "Customer",
        back_populates="addresses"
    )

    def __init__(
        self,
        customer_id,
        customer_address,
        customer_city,
        customer_state,
        customer_pincode,
        country,
        is_default=False
    ):

        self.customer_id = customer_id
        self.address_line1 = customer_address
        self.city = customer_city
        self.state = customer_state
        self.postal_code = customer_pincode
        self.country = country
        self.is_default = is_default

    def __str__(self):

        return (
            f"Address ID : {self.address_id}\n"
            f"Customer ID : {self.customer_id}\n"
            f"Address : {self.address_line1}\n"
            f"City : {self.city}\n"
            f"State : {self.state}\n"
            f"Pincode : {self.postal_code}\n"
            f"Country : {self.country}"
        )