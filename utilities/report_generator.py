"""
File : report_generator.py
Description : Formatting/printing helpers for reports produced by
              services/report_service.py. Keeps display logic out
              of the service layer so report_service stays pure
              data (list/dict) and easy to test.
"""


def print_monthly_sales_report(data):
    print("\n========== MONTHLY SALES REPORT ==========")

    if isinstance(data, str):
        print(data)
        return

    if not data:
        print("No sales data available.")
        return

    print(f"{'Month':<10}{'Total Revenue':>15}")
    print("-" * 25)

    for row in data:
        print(f"{row['month']:<10}{row['total_revenue']:>15,.2f}")


def print_best_selling_products(data):
    print("\n========== BEST SELLING PRODUCTS ==========")

    if isinstance(data, str):
        print(data)
        return

    if not data:
        print("No sales data available.")
        return

    for i, row in enumerate(data, start=1):
        print(f"{i}. {row['product_name']} — {row['units_sold']} units sold")


def print_customer_purchase_history(data):
    print("\n========== CUSTOMER PURCHASE HISTORY ==========")

    if isinstance(data, str):
        print(data)
        return

    print(f"Customer : {data['customer_name']}")

    if not data["orders"]:
        print("No orders placed yet.")
        return

    for i, order in enumerate(data["orders"], start=1):
        print(
            f"Order {i} — #{order['order_id']} | "
            f"{order['order_date']} | {order['status']} | "
            f"₹{order['total_amount']:,.2f}"
        )


def print_pending_orders(data):
    print("\n========== PENDING ORDERS ==========")

    if isinstance(data, str):
        print(data)
        return

    if not data:
        print("No pending orders.")
        return

    for row in data:
        print(
            f"Order #{row['order_id']} | {row['customer_name']} | "
            f"{row['order_date']} | ₹{row['total_amount']:,.2f}"
        )


def print_revenue_by_category(data):
    print("\n========== REVENUE BY CATEGORY ==========")

    if isinstance(data, str):
        print(data)
        return

    if not data:
        print("No revenue data available.")
        return

    print(f"{'Category':<20}{'Revenue':>15}")
    print("-" * 35)

    for row in data:
        print(f"{row['category_name']:<20}{row['revenue']:>15,.2f}")


def print_low_stock_products_report(data):
    print("\n========== LOW STOCK PRODUCTS ==========")

    if isinstance(data, str):
        print(data)
        return

    if not data:
        print("No products are low on stock.")
        return

    for row in data:
        print(
            f"{row['product_name']:<20} | "
            f"Qty: {row['quantity']:<5} | "
            f"Threshold: {row['threshold']}"
        )