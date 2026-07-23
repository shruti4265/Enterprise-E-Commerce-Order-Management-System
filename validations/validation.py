class InventoryValidation:

    @staticmethod
    def validate_product_id(product_id):

        if product_id <= 0:
            raise ValueError(
                "Product ID must be greater than zero."
            )

    @staticmethod
    def validate_quantity(quantity):

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

    @staticmethod
    def validate_low_stock_threshold(threshold):

        if threshold < 0:
            raise ValueError(
                "Low stock threshold cannot be negative."
            )

    @staticmethod
    def validate_available_quantity(
        available_quantity,
        requested_quantity
    ):

        if requested_quantity > available_quantity:
            raise ValueError(
                "Insufficient stock available."
            )