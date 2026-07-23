from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from models.inventory_model import Inventory
from models.stock_transaction_model import StockTransaction
from models.product_model import Product
from validations.validation import InventoryValidation


class InventoryService:

    def __init__(self):
        self.database_session = SessionLocal()

    # ==========================================================
    # Add Stock
    # ==========================================================

    def add_stock(self, product_id, quantity, reason="Stock Added"):

        InventoryValidation.validate_product_id(product_id)
        InventoryValidation.validate_quantity(quantity)

        try:

            existing_product = self.database_session.scalar(
                select(Product).where(
                    Product.product_id == product_id
                )
            )

            if existing_product is None:
                print("Product not found.")
                return

            inventory = self.database_session.scalar(
                select(Inventory).where(
                    Inventory.product_id == product_id
                )
            )

            if inventory:

                inventory.quantity += quantity

            else:

                inventory = Inventory(
                    product_id=product_id,
                    quantity=quantity,
                    low_stock_threshold=10
                )

                self.database_session.add(inventory)

            transaction = StockTransaction(
                product_id=product_id,
                change_qty=quantity,
                transaction_type="IN",
                reason=reason
            )

            self.database_session.add(transaction)

            self.database_session.commit()

            print("Stock added successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # Remove Stock
    # ==========================================================

    def remove_stock(self, product_id, quantity, reason="Stock Removed"):

        InventoryValidation.validate_product_id(product_id)
        InventoryValidation.validate_quantity(quantity)

        try:

            inventory = self.database_session.scalar(
                select(Inventory).where(
                    Inventory.product_id == product_id
                )
            )

            if inventory is None:

                print("Inventory record not found.")
                return

            InventoryValidation.validate_available_quantity(
                inventory.quantity,
                quantity
            )

            inventory.quantity -= quantity

            transaction = StockTransaction(
                product_id=product_id,
                change_qty=-quantity,
                transaction_type="OUT",
                reason=reason
            )

            self.database_session.add(transaction)

            self.database_session.commit()

            print("Stock removed successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)
            
    # ==========================================================
    # Update Stock
    # ==========================================================

    def update_stock(self, product_id, new_quantity, reason="Stock Adjusted"):

        InventoryValidation.validate_product_id(product_id)
        InventoryValidation.validate_quantity(new_quantity)

        try:

            inventory = self.database_session.scalar(
                select(Inventory).where(
                    Inventory.product_id == product_id
                )
            )

            if inventory is None:
                print("Inventory record not found.")
                return

            difference = new_quantity - inventory.quantity

            inventory.quantity = new_quantity

            transaction = StockTransaction(
                product_id=product_id,
                change_qty=difference,
                transaction_type="ADJUSTMENT",
                reason=reason
            )

            self.database_session.add(transaction)

            self.database_session.commit()

            print("Inventory updated successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()
            print(error)

    # ==========================================================
    # View Stock
    # ==========================================================

    def view_stock(self, product_id):

        InventoryValidation.validate_product_id(product_id)

        try:

            inventory = self.database_session.scalar(
                select(Inventory).where(
                    Inventory.product_id == product_id
                )
            )

            if inventory is None:
                print("Inventory record not found.")
                return

            print("\n========== STOCK DETAILS ==========")
            print(f"Inventory ID        : {inventory.inventory_id}")
            print(f"Product ID          : {inventory.product_id}")
            print(f"Quantity            : {inventory.quantity}")
            print(f"Low Stock Threshold : {inventory.low_stock_threshold}")
            print(f"Last Updated        : {inventory.updated_at}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # View Inventory
    # ==========================================================

    def view_inventory(self):

        try:

            inventory_list = self.database_session.scalars(
                select(Inventory)
            ).all()

            if not inventory_list:
                print("No inventory records found.")
                return

            print("\n============= INVENTORY =============")

            for inventory in inventory_list:

                print("--------------------------------------")
                print(f"Inventory ID : {inventory.inventory_id}")
                print(f"Product ID   : {inventory.product_id}")
                print(f"Quantity     : {inventory.quantity}")
                print(f"Threshold    : {inventory.low_stock_threshold}")
                print(f"Updated At   : {inventory.updated_at}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Low Stock Products
    # ==========================================================

    def low_stock_products(self):

        try:

            low_stock_list = self.database_session.scalars(
                select(Inventory).where(
                    Inventory.quantity <= Inventory.low_stock_threshold
                )
            ).all()

            if not low_stock_list:
                print("No low stock products found.")
                return

            print("\n========== LOW STOCK PRODUCTS ==========")

            for inventory in low_stock_list:

                print("----------------------------------------")
                print(f"Product ID : {inventory.product_id}")
                print(f"Quantity   : {inventory.quantity}")
                print(f"Threshold  : {inventory.low_stock_threshold}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Stock History
    # ==========================================================

    def stock_history(self, product_id=None):

        try:

            if product_id:

                transaction_list = self.database_session.scalars(
                    select(StockTransaction).where(
                        StockTransaction.product_id == product_id
                    )
                ).all()

            else:

                transaction_list = self.database_session.scalars(
                    select(StockTransaction)
                ).all()

            if not transaction_list:
                print("No stock transactions found.")
                return

            print("\n========== STOCK TRANSACTION HISTORY ==========")

            for transaction in transaction_list:

                print("-----------------------------------------------")
                print(f"Transaction ID : {transaction.transaction_id}")
                print(f"Product ID     : {transaction.product_id}")
                print(f"Change Qty     : {transaction.change_qty}")
                print(f"Type           : {transaction.transaction_type}")
                print(f"Reason         : {transaction.reason}")
                print(f"Created At     : {transaction.created_at}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Close Session
    # ==========================================================

    def close_session(self):

        self.database_session.close()