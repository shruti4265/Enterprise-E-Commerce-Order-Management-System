class PaymentValidation:

    @staticmethod
    def validate_payment_id(payment_id):

        if payment_id <= 0:
            raise ValueError(
                "Payment ID must be greater than zero."
            )

    @staticmethod
    def validate_order_id(order_id):

        if order_id <= 0:
            raise ValueError(
                "Order ID must be greater than zero."
            )

    @staticmethod
    def validate_amount(amount):

        if amount <= 0:
            raise ValueError(
                "Payment amount must be greater than zero."
            )

    @staticmethod
    def validate_payment_method(payment_method):

        if not payment_method.strip():
            raise ValueError(
                "Payment method cannot be empty."
            )

    @staticmethod
    def validate_payment_status(payment_status):

        valid_status = [
            "Pending",
            "Paid",
            "Failed",
            "Refunded"
        ]

        if payment_status not in valid_status:
            raise ValueError(
                "Invalid payment status."
            )

    @staticmethod
    def validate_shipment_id(shipment_id):

        if shipment_id <= 0:
            raise ValueError(
                "Shipment ID must be greater than zero."
            )

    @staticmethod
    def validate_tracking_number(tracking_number):

        if not tracking_number.strip():
            raise ValueError(
                "Tracking number cannot be empty."
            )

    @staticmethod
    def validate_courier_name(courier_name):

        if not courier_name.strip():
            raise ValueError(
                "Courier name cannot be empty."
            )

    @staticmethod
    def validate_shipment_status(shipment_status):

        valid_status = [
            "Pending",
            "Shipped",
            "Out for Delivery",
            "Delivered",
            "Cancelled"
        ]

        if shipment_status not in valid_status:
            raise ValueError(
                "Invalid shipment status."
            )