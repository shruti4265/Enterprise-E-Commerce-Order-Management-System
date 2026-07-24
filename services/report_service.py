"""
File : report_service.py
Description : Reports & Analytics Service Layer

Uses SQLAlchemy ORM against the models already merged into main
(Category, Product, Inventory, Order, OrderItem).

NOTE ON CUSTOMERS:
Customer Management (models/customer_model.py) has not been built yet,
so there is no ORM `Customer` class to query. The two reports below that
need customer info (customer_purchase_history, pending_orders) fall back
to raw SQL against the `customers` table defined in schema.sql
(columns: customer_id, name, email).

ACTION REQUIRED once customer_model.py exists:
    - Replace the raw SQL blocks marked "TEMP: raw SQL" with proper
      ORM joins against the real Customer model.
    - Confirm the actual column name the Customer model uses for the
      person's name (schema.sql uses `name`, but note that Category/
      Product use a prefixed style: `category_name` / `product_name`.
      If Customer follows that same pattern it may be `customer_name`
      instead of `name` -- check before wiring the ORM join.
"""

import logging

from sqlalchemy import func, text
from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from models.order_model import Order
from models.order_item_model import OrderItem
from models.product_model import Product
from models.category_model import Category
from models.inventory_model import Inventory

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ---------------------------- 1. MONTHLY SALES REPORT ---------------------------- #

def monthly_sales_report():
    """
    Total revenue grouped by month, based on non-cancelled orders.
    Returns a list of dicts: [{"month": "2026-01", "total_revenue": 250000.0}, ...]
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                func.date_format(Order.order_date, "%Y-%m").label("month"),
                func.sum(Order.total_amount).label("total_revenue")
            )
            .filter(Order.order_status != "Cancelled")
            .group_by("month")
            .order_by("month")
            .all()
        )

        report = [
            {"month": row.month, "total_revenue": float(row.total_revenue or 0)}
            for row in results
        ]

        logger.info("Monthly Sales Report Generated.")
        return report

    except SQLAlchemyError as e:
        logger.error(f"Error generating monthly sales report: {e}")
        return f"Error generating monthly sales report: {e}"

    finally:
        session.close()


# ---------------------------- 2. BEST SELLING PRODUCTS ---------------------------- #

def best_selling_products(limit=10):
    """
    Products ranked by total quantity sold across all order items.
    Returns a list of dicts: [{"product_name": "Laptop", "units_sold": 120}, ...]
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Product.product_name,
                func.sum(OrderItem.quantity).label("units_sold")
            )
            .join(OrderItem, OrderItem.product_id == Product.product_id)
            .group_by(Product.product_id, Product.product_name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
            .all()
        )

        report = [
            {"product_name": row.product_name, "units_sold": int(row.units_sold or 0)}
            for row in results
        ]

        logger.info("Best Selling Products Report Generated.")
        return report

    except SQLAlchemyError as e:
        logger.error(f"Error generating best selling products report: {e}")
        return f"Error generating best selling products report: {e}"

    finally:
        session.close()


# ---------------------------- 3. CUSTOMER PURCHASE HISTORY ---------------------------- #

def customer_purchase_history(customer_id):
    """
    All orders placed by a given customer, most recent first.
    Returns a dict: {"customer_name": ..., "orders": [{...}, ...]}

    TEMP: raw SQL for the customer name lookup, see module docstring.
    """

    session = SessionLocal()

    try:
        # TEMP: raw SQL until Customer ORM model exists
        customer_row = session.execute(
            text("SELECT name, email FROM customers WHERE customer_id = :cid"),
            {"cid": customer_id}
        ).first()

        if customer_row is None:
            logger.warning(f"No customer found with id {customer_id}.")
            return f"No customer found with id {customer_id}."

        orders = (
            session.query(Order)
            .filter(Order.customer_id == customer_id)
            .order_by(Order.order_date.desc())
            .all()
        )

        order_list = [
            {
                "order_id": o.order_id,
                "order_date": o.order_date,
                "status": o.order_status,
                "total_amount": o.total_amount,
            }
            for o in orders
        ]

        logger.info(f"Purchase History Retrieved for Customer {customer_id}.")
        return {"customer_name": customer_row.name, "orders": order_list}

    except SQLAlchemyError as e:
        logger.error(f"Error generating customer purchase history: {e}")
        return f"Error generating customer purchase history: {e}"

    finally:
        session.close()


# ---------------------------- 4. PENDING ORDERS ---------------------------- #

def pending_orders():
    """
    All orders currently in 'Pending' status, with customer name attached.
    Returns a list of dicts.

    TEMP: raw SQL joined against customers, see module docstring.
    """

    session = SessionLocal()

    try:
        rows = session.execute(
            text(
                """
                SELECT
                    orders.order_id,
                    orders.order_date,
                    orders.total_amount,
                    customers.name AS customer_name
                FROM orders
                JOIN customers ON customers.customer_id = orders.customer_id
                WHERE orders.order_status = 'Pending'
                ORDER BY orders.order_date
                """
            )
        ).mappings().all()

        report = [dict(row) for row in rows]

        logger.info("Pending Orders Report Generated.")
        return report

    except SQLAlchemyError as e:
        logger.error(f"Error generating pending orders report: {e}")
        return f"Error generating pending orders report: {e}"

    finally:
        session.close()


# ---------------------------- 5. REVENUE BY CATEGORY ---------------------------- #

def revenue_by_category():
    """
    Total revenue grouped by product category.
    Returns a list of dicts: [{"category_name": "Electronics", "revenue": 500000.0}, ...]
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Category.category_name,
                func.sum(OrderItem.subtotal).label("revenue")
            )
            .join(Product, Product.category_id == Category.category_id)
            .join(OrderItem, OrderItem.product_id == Product.product_id)
            .group_by(Category.category_id, Category.category_name)
            .order_by(func.sum(OrderItem.subtotal).desc())
            .all()
        )

        report = [
            {"category_name": row.category_name, "revenue": float(row.revenue or 0)}
            for row in results
        ]

        logger.info("Revenue by Category Report Generated.")
        return report

    except SQLAlchemyError as e:
        logger.error(f"Error generating revenue by category report: {e}")
        return f"Error generating revenue by category report: {e}"

    finally:
        session.close()


# ---------------------------- 6. LOW STOCK PRODUCTS ---------------------------- #

def low_stock_products_report():
    """
    Products whose current inventory is at or below their low stock threshold.
    Returns a list of dicts: [{"product_name": ..., "quantity": ..., "threshold": ...}, ...]
    """

    session = SessionLocal()

    try:
        results = (
            session.query(
                Product.product_name,
                Inventory.quantity,
                Inventory.low_stock_threshold
            )
            .join(Inventory, Inventory.product_id == Product.product_id)
            .filter(Inventory.quantity <= Inventory.low_stock_threshold)
            .order_by(Inventory.quantity)
            .all()
        )

        report = [
            {
                "product_name": row.product_name,
                "quantity": row.quantity,
                "threshold": row.low_stock_threshold,
            }
            for row in results
        ]

        logger.info("Low Stock Products Report Generated.")
        return report

    except SQLAlchemyError as e:
        logger.error(f"Error generating low stock products report: {e}")
        return f"Error generating low stock products report: {e}"

    finally:
        session.close()