from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from database import SessionLocal
from models.cart_model import Cart
from models.cart_item_model import CartItem
from models.order_model import Order
from models.order_item_model import OrderItem

from models.product_model import Product
from models.inventory_model import Inventory
from models.customer_model import Customer



class OrderService:

    def __init__(self):

        self.database_session = SessionLocal()

    # ==========================================================
    # Create Cart
    # ==========================================================

    def create_cart(self, customer_id):

        try:

            # Check whether the customer exists
            customer = self.database_session.scalar(
                select(Customer).where(
                    Customer.customer_id == customer_id
                )
            )

            if customer is None:
                print("Customer not found.")
                return

            # Check whether the customer already has a cart
            existing_cart = self.database_session.scalar(
                select(Cart).where(
                    Cart.customer_id == customer_id
                )
            )

            if existing_cart:
                print("Cart already exists.")
                return existing_cart

            # Create a new cart
            cart = Cart(
                customer_id=customer_id
            )

            self.database_session.add(cart)
            self.database_session.commit()
            self.database_session.refresh(cart)

            print("Cart created successfully.")
            return cart

        except SQLAlchemyError as error:

            self.database_session.rollback()
            print(f"Database Error: {error}")
    # ==========================================================
    # Add Product To Cart
    # ==========================================================

    def add_to_cart(self,
                    customer_id,
                    product_id,
                    quantity):

        try:

            product = self.database_session.scalar(

                select(Product).where(
                    Product.product_id == product_id
                )

            )

            if product is None:

                print("Product not found.")

                return

            inventory = self.database_session.scalar(

                select(Inventory).where(
                    Inventory.product_id == product_id
                )

            )

            if inventory is None:

                print("Inventory record not found.")

                return

            if inventory.quantity < quantity:

                print("Insufficient stock available.")

                return

            cart = self.database_session.scalar(

                select(Cart).where(
                    Cart.customer_id == customer_id
                )

            )

            if cart is None:

                cart = Cart(

                    customer_id=customer_id

                )

                self.database_session.add(cart)

                self.database_session.commit()

            subtotal = quantity * product.price

            cart_item = CartItem(

                cart_id=cart.cart_id,

                product_id=product_id,

                quantity=quantity,

                unit_price=product.price,

                subtotal=subtotal

            )

            self.database_session.add(cart_item)

            self.database_session.commit()

            print("Product added to cart successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)
            
    # ==========================================================
    # View Cart
    # ==========================================================

    def view_cart(self, customer_id):

        try:

            cart = self.database_session.scalar(

                select(Cart).where(
                    Cart.customer_id == customer_id
                )

            )

            if cart is None:

                print("Cart not found.")

                return

            cart_items = self.database_session.scalars(

                select(CartItem).where(
                    CartItem.cart_id == cart.cart_id
                )

            ).all()

            if not cart_items:

                print("Cart is empty.")

                return

            print("\n========== CART ==========")

            total = 0

            for item in cart_items:

                print("----------------------------------")
                print(f"Cart Item ID : {item.cart_item_id}")
                print(f"Product ID   : {item.product_id}")
                print(f"Quantity     : {item.quantity}")
                print(f"Unit Price   : {item.unit_price}")
                print(f"Subtotal     : {item.subtotal}")

                total += item.subtotal

            print("----------------------------------")
            print(f"Cart Total : {total}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Update Cart Item Quantity
    # ==========================================================

    def update_cart_item(
            self,
            cart_item_id,
            quantity
    ):

        try:

            cart_item = self.database_session.scalar(

                select(CartItem).where(
                    CartItem.cart_item_id == cart_item_id
                )

            )

            if cart_item is None:

                print("Cart Item not found.")

                return

            inventory = self.database_session.scalar(

                select(Inventory).where(
                    Inventory.product_id == cart_item.product_id
                )

            )

            if inventory.quantity < quantity:

                print("Insufficient stock.")

                return

            cart_item.quantity = quantity

            cart_item.subtotal = (
                quantity *
                cart_item.unit_price
            )

            self.database_session.commit()

            print("Cart updated successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # Remove Product From Cart
    # ==========================================================

    def remove_cart_item(self, cart_item_id):

        try:

            cart_item = self.database_session.scalar(

                select(CartItem).where(
                    CartItem.cart_item_id == cart_item_id
                )

            )

            if cart_item is None:

                print("Cart Item not found.")

                return

            self.database_session.delete(cart_item)

            self.database_session.commit()

            print("Product removed from cart.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)
            
            
                # ==========================================================
    # Place Order
    # ==========================================================

    def place_order(self, customer_id):

        try:

            cart = self.database_session.scalar(

                select(Cart).where(
                    Cart.customer_id == customer_id
                )

            )

            if cart is None:

                print("Cart not found.")

                return

            cart_items = self.database_session.scalars(

                select(CartItem).where(
                    CartItem.cart_id == cart.cart_id
                )

            ).all()

            if not cart_items:

                print("Cart is empty.")

                return

            total_amount = 0

            for item in cart_items:

                total_amount += item.subtotal

            order = Order(

                customer_id=customer_id,

                total_amount=total_amount,

                order_status="Pending"

            )

            self.database_session.add(order)

            self.database_session.commit()

            for item in cart_items:

                order_item = OrderItem(

                    order_id=order.order_id,

                    product_id=item.product_id,

                    quantity=item.quantity,

                    unit_price=item.unit_price,

                    subtotal=item.subtotal

                )

                self.database_session.add(order_item)

                inventory = self.database_session.scalar(

                    select(Inventory).where(
                        Inventory.product_id == item.product_id
                    )

                )

                inventory.quantity -= item.quantity

            for item in cart_items:

                self.database_session.delete(item)

            self.database_session.commit()

            print("Order placed successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # View Orders
    # ==========================================================

    def view_orders(self, customer_id):

        try:

            order_list = self.database_session.scalars(

                select(Order).where(
                    Order.customer_id == customer_id
                )

            ).all()

            if not order_list:

                print("No orders found.")

                return

            print("\n========== ORDERS ==========")

            for order in order_list:

                print("--------------------------------------")
                print(f"Order ID      : {order.order_id}")
                print(f"Order Date    : {order.order_date}")
                print(f"Total Amount  : {order.total_amount}")
                print(f"Order Status  : {order.order_status}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # View Order Details
    # ==========================================================

    def view_order_details(self, order_id):

        try:

            order_items = self.database_session.scalars(

                select(OrderItem).where(
                    OrderItem.order_id == order_id
                )

            ).all()

            if not order_items:

                print("Order not found.")

                return

            print("\n========== ORDER DETAILS ==========")

            for item in order_items:

                print("-----------------------------------")
                print(f"Product ID : {item.product_id}")
                print(f"Quantity   : {item.quantity}")
                print(f"Unit Price : {item.unit_price}")
                print(f"Subtotal   : {item.subtotal}")

        except SQLAlchemyError as error:

            print(error)

    # ==========================================================
    # Cancel Order
    # ==========================================================

    def cancel_order(self, order_id):

        try:

            order = self.database_session.scalar(

                select(Order).where(
                    Order.order_id == order_id
                )

            )

            if order is None:

                print("Order not found.")

                return

            order.order_status = "Cancelled"

            self.database_session.commit()

            print("Order cancelled successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # Clear Cart
    # ==========================================================

    def clear_cart(self, customer_id):

        try:

            cart = self.database_session.scalar(

                select(Cart).where(
                    Cart.customer_id == customer_id
                )

            )

            if cart is None:

                print("Cart not found.")

                return

            cart_items = self.database_session.scalars(

                select(CartItem).where(
                    CartItem.cart_id == cart.cart_id
                )

            ).all()

            for item in cart_items:

                self.database_session.delete(item)

            self.database_session.commit()

            print("Cart cleared successfully.")

        except SQLAlchemyError as error:

            self.database_session.rollback()

            print(error)

    # ==========================================================
    # Close Session
    # ==========================================================

    def close_session(self):

        self.database_session.close()