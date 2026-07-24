from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from models.payment_model import Payment
from models.shipment_model import Shipment
from models.order_model import Order
from models.address_model import Address


class PaymentService:

    def __init__(self):

        self.database_session = SessionLocal()

    # ==========================================================
    # Make Payment
    # ==========================================================

    def make_payment(
        self,
        order_id,
        amount,
        payment_method
    ):

        try:

            payment = Payment(
                order_id=order_id,
                amount=amount,
                payment_method=payment_method,
                payment_status="SUCCESS"
            )

            self.database_session.add(payment)

            self.database_session.commit()

            print("Payment recorded successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # Verify Payment
    # ==========================================================

    def verify_payment(self, payment_id):

        try:

            payment = self.database_session.scalar(
                select(Payment).where(
                    Payment.payment_id == payment_id
                )
            )

            if payment is None:

                print("Payment not found.")
                return

            print("\n========== PAYMENT DETAILS ==========")
            print(f"Payment ID     : {payment.payment_id}")
            print(f"Order ID       : {payment.order_id}")
            print(f"Amount         : {payment.amount}")
            print(f"Method         : {payment.payment_method}")
            print(f"Status         : {payment.payment_status}")
            print(f"Payment Date   : {payment.payment_date}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Payment History
    # ==========================================================

    def payment_history(self):

        try:

            payments = self.database_session.scalars(
                select(Payment)
            ).all()

            if not payments:

                print("No payment records found.")
                return

            print("\n========== PAYMENT HISTORY ==========")

            for payment in payments:

                print("--------------------------------------")
                print(f"Payment ID : {payment.payment_id}")
                print(f"Order ID   : {payment.order_id}")
                print(f"Amount     : {payment.amount}")
                print(f"Method     : {payment.payment_method}")
                print(f"Status     : {payment.payment_status}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Refund Payment
    # ==========================================================

    def refund_payment(self, payment_id):

        try:

            payment = self.database_session.scalar(
                select(Payment).where(
                    Payment.payment_id == payment_id
                )
            )

            if payment is None:

                print("Payment not found.")
                return

            payment.payment_status = "REFUNDED"

            self.database_session.commit()

            print("Refund processed successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # Create Shipment
    # ==========================================================

    def create_shipment(
        self,
        order_id,
        address_id,
        tracking_number
    ):

        try:

            order = self.database_session.scalar(
                select(Order).where(
                    Order.order_id == order_id
                )
            )

            if order is None:
                print("Order not found.")
                return

            address = self.database_session.scalar(
                select(Address).where(
                    Address.address_id == address_id
                )
            )

            if address is None:
                print("Address not found.")
                return

            shipment = Shipment(
                order_id=order_id,
                address_id=address_id,
                tracking_number=tracking_number,
                shipment_status="PROCESSING"
            )

            self.database_session.add(shipment)

            self.database_session.commit()

            print("Shipment created successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)    
    # ==========================================================
    # Update Shipment
    # ==========================================================

    def update_shipment(
        self,
        shipment_id,
        shipment_status
    ):

        try:

            shipment = self.database_session.scalar(
                select(Shipment).where(
                    Shipment.shipment_id == shipment_id
                )
            )

            if shipment is None:

                print("Shipment not found.")
                return

            shipment.shipment_status = shipment_status

            self.database_session.commit()

            print("Shipment updated successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # Track Shipment
    # ==========================================================

    def track_shipment(self, shipment_id):

        try:

            shipment = self.database_session.scalar(
                select(Shipment).where(
                    Shipment.shipment_id == shipment_id
                )
            )

            if shipment is None:

                print("Shipment not found.")
                return

            print("\n========== SHIPMENT DETAILS ==========")
            print(f"Shipment ID     : {shipment.shipment_id}")
            print(f"Order ID        : {shipment.order_id}")
            print(f"Tracking Number : {shipment.tracking_number}")
            print(f"Address ID      : {shipment.address_id}")
            print(f"Status          : {shipment.shipment_status}")
            print(f"Shipped Date    : {shipment.shipped_date}")
            print(f"Delivered Date  : {shipment.delivered_date}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Delivery Status
    # ==========================================================

    def delivery_status(self):

        try:

            shipments = self.database_session.scalars(
                select(Shipment)
            ).all()

            if not shipments:

                print("No shipment records found.")
                return

            print("\n========== DELIVERY STATUS ==========")

            for shipment in shipments:

                print("--------------------------------------")
                print(f"Shipment ID : {shipment.shipment_id}")
                print(f"Order ID    : {shipment.order_id}")
                print(f"Status      : {shipment.shipment_status}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Close Session
    # ==========================================================

    def close_session(self):

        self.database_session.close()