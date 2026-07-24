"""
main.py

Entry point for the Enterprise E-Commerce Order Management System.
"""

from database_initializer import init_db
from services.customer_service import (
    add_customer,
    view_all_customers,
    view_customer,
    search_customer,
    update_customer,
    delete_customer,
)
from services.product_service import (
    add_category,
    view_categories,
    update_category,
    delete_category,
    add_product,
    update_product,
    delete_product,
    view_product,
    view_all_products,
    search_product,
    search_by_category,
)
from services.report_service import (
    monthly_sales_report,
    best_selling_products,
    customer_purchase_history,
    pending_orders,
    revenue_by_category,
    low_stock_products_report,
)
from services.inventory_service import InventoryService
from exceptions.custom_exception import ValidationError, DatabaseError
from services.order_service import OrderService
from services.payment_service import PaymentService



def display_menu():
    print("\n" + "=" * 60)
    print("    ENTERPRISE E-COMMERCE ORDER MANAGEMENT SYSTEM")
    print("=" * 60)
    print("1. Customer Management")
    print("2. Product Management")
    print("3. Inventory Management")
    print("4. Cart & Order Management")
    print("5. Payment & Shipment")
    print("6. Reports")
    print("0. Exit")
    print("=" * 60)


def customer_menu():
    while True:
        print("\n" + "-" * 60)
        print("    CUSTOMER MANAGEMENT")
        print("-" * 60)
        print("1. Add Customer")
        print("2. View All Customers")
        print("3. View Customer by ID")
        print("4. Search Customer")
        print("5. Update Customer")
        print("6. Delete Customer")
        print("0. Back to Main Menu")
        print("-" * 60)

        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Name: ").strip()
                email = input("Email: ").strip()
                phone = input("Phone: ").strip()
                customer = add_customer(name, email, phone)
                print(f"\nCustomer added successfully. ID: {customer.customer_id}")

            elif choice == "2":
                customers = view_all_customers()
                if not customers:
                    print("\nNo customers found.")
                for c in customers:
                    print("\n" + str(c))

            elif choice == "3":
                customer_id = input("Customer ID: ").strip()
                customer = view_customer(int(customer_id))
                print("\n" + str(customer))

            elif choice == "4":
                search_value = input("Search (name/email/phone): ").strip()
                results = search_customer(search_value)
                if not results:
                    print("\nNo matching customers found.")
                for c in results:
                    print("\n" + str(c))

            elif choice == "5":
                customer_id = input("Customer ID to update: ").strip()
                name = input("New Name: ").strip()
                email = input("New Email: ").strip()
                phone = input("New Phone: ").strip()
                customer = update_customer(int(customer_id), name, email, phone)
                print(f"\nCustomer {customer.customer_id} updated successfully.")

            elif choice == "6":
                customer_id = input("Customer ID to delete: ").strip()
                delete_customer(int(customer_id))
                print("\nCustomer deleted successfully.")

            elif choice == "0":
                break

            else:
                print("\nInvalid choice. Please try again.")

        except ValueError:
            print("\nCustomer ID must be a number.")
        except ValidationError as e:
            print(f"\nValidation error: {e}")
        except DatabaseError as e:
            print(f"\nDatabase error: {e}")

def handle_product_menu():
    while True:
        print("\n--- Product Management ---")
        print("1. Add Category")
        print("2. View Categories")
        print("3. Add Product")
        print("4. View All Products")
        print("5. Search Product")
        print("6. Update Product")
        print("7. Delete Product")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            name = input("Category name: ").strip()
            print(add_category(name))

        elif choice == "2":
            for c in view_categories():
                print(f"{c.category_id} - {c.name}")

        elif choice == "3":
            name = input("Product name: ").strip()
            desc = input("Description: ").strip()
            price = float(input("Price: ").strip())
            qty = int(input("Initial quantity: ").strip())
            active = input("Active? (y/n): ").strip().lower() == "y"
            cat_id = int(input("Category ID: ").strip())
            print(add_product(name, desc, price, qty, active, cat_id))

        elif choice == "4":
            for p in view_all_products():
                print(p)

        elif choice == "5":
            val = input("Search by name or ID: ").strip()
            for p in search_product(val):
                print(p)
        elif choice == "6":
            pid = int(input("Product ID to update: ").strip())
            name = input("New name: ").strip()
            desc = input("New description: ").strip()
            price = float(input("New price: ").strip())
            active = input("Active? (y/n): ").strip().lower() == "y"
            cat_id = int(input("New category ID: ").strip())
            print(update_product(pid, name, desc, price, active, cat_id))

        elif choice == "7":
            pid = int(input("Product ID to delete: ").strip())
            print(delete_product(pid))

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
def handle_inventory_menu():
    inventory_service = InventoryService()

    while True:
        print("\n--- Inventory Management ---")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Update Stock")
        print("4. View Stock (by Product ID)")
        print("5. View All Inventory")
        print("6. Low Stock Products")
        print("7. Stock Transaction History")
        print("0. Back to Main Menu")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            pid = int(input("Product ID: ").strip())
            qty = int(input("Quantity to add: ").strip())
            reason = input("Reason (optional, press Enter to skip): ").strip() or "Stock Added"
            inventory_service.add_stock(pid, qty, reason)

        elif choice == "2":
            pid = int(input("Product ID: ").strip())
            qty = int(input("Quantity to remove: ").strip())
            reason = input("Reason (optional, press Enter to skip): ").strip() or "Stock Removed"
            inventory_service.remove_stock(pid, qty, reason)

        elif choice == "3":
            pid = int(input("Product ID: ").strip())
            qty = int(input("New quantity: ").strip())
            reason = input("Reason (optional, press Enter to skip): ").strip() or "Stock Adjusted"
            inventory_service.update_stock(pid, qty, reason)

        elif choice == "4":
            pid = int(input("Product ID: ").strip())
            inventory_service.view_stock(pid)

        elif choice == "5":
            inventory_service.view_inventory()

        elif choice == "6":
            inventory_service.low_stock_products()

        elif choice == "7":
            pid_input = input("Product ID (press Enter for full history): ").strip()
            pid = int(pid_input) if pid_input else None
            inventory_service.stock_history(pid)

        elif choice == "0":
            inventory_service.close_session()
            break

        else:
            print("Invalid choice.")
def handle_cart_order_menu():
    order_service = OrderService()

    while True:
        print("\n--- Cart & Order Management ---")
        print("1. Create Cart")
        print("2. Add Product to Cart")
        print("3. View Cart")
        print("4. Update Cart Item")
        print("5. Remove Cart Item")
        print("6. Place Order")
        print("7. View Orders")
        print("8. View Order Details")
        print("9. Cancel Order")
        print("10. Clear Cart")
        print("0. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            customer_id = int(input("Customer ID: "))
            order_service.create_cart(customer_id)

        elif choice == "2":
            customer_id = int(input("Customer ID: "))
            product_id = int(input("Product ID: "))
            quantity = int(input("Quantity: "))
            order_service.add_to_cart(customer_id, product_id, quantity)

        elif choice == "3":
            customer_id = int(input("Customer ID: "))
            order_service.view_cart(customer_id)

        elif choice == "4":
            cart_item_id = int(input("Cart Item ID: "))
            quantity = int(input("New Quantity: "))
            order_service.update_cart_item(cart_item_id, quantity)

        elif choice == "5":
            cart_item_id = int(input("Cart Item ID: "))
            order_service.remove_cart_item(cart_item_id)

        elif choice == "6":
            customer_id = int(input("Customer ID: "))
            order_service.place_order(customer_id)

        elif choice == "7":
            customer_id = int(input("Customer ID: "))
            order_service.view_orders(customer_id)

        elif choice == "8":
            order_id = int(input("Order ID: "))
            order_service.view_order_details(order_id)

        elif choice == "9":
            order_id = int(input("Order ID: "))
            order_service.cancel_order(order_id)

        elif choice == "10":
            customer_id = int(input("Customer ID: "))
            order_service.clear_cart(customer_id)

        elif choice == "0":
            order_service.close_session()
            break

        else:
            print("Invalid choice.")
def handle_payment_shipment_menu():

    payment_service = PaymentService()

    while True:

        print("\n--- Payment & Shipment ---")
        print("1. Make Payment")
        print("2. Verify Payment")
        print("3. Payment History")
        print("4. Refund Payment")
        print("5. Create Shipment")
        print("6. Update Shipment")
        print("7. Track Shipment")
        print("8. Delivery Status")
        print("0. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            order_id = int(input("Order ID: "))
            amount = float(input("Amount: "))

            print("\nPayment Methods")
            print("CARD")
            print("UPI")
            print("NET_BANKING")
            print("COD")
            print("WALLET")

            payment_method = input("Payment Method: ").strip().upper()

            payment_service.make_payment(
                order_id,
                amount,
                payment_method
            )

        elif choice == "2":

            payment_id = int(input("Payment ID: "))
            payment_service.verify_payment(payment_id)

        elif choice == "3":

            payment_service.payment_history()

        elif choice == "4":

            payment_id = int(input("Payment ID: "))
            payment_service.refund_payment(payment_id)

        elif choice == "5":

            order_id = int(input("Order ID: "))
            address_id = int(input("Address ID: "))
            tracking_number = input("Tracking Number: ").strip()

            payment_service.create_shipment(
                order_id,
                address_id,
                tracking_number
            )

        elif choice == "6":

            shipment_id = int(input("Shipment ID: "))

            print("\nShipment Status")
            print("PROCESSING")
            print("SHIPPED")
            print("OUT_FOR_DELIVERY")
            print("DELIVERED")
            print("RETURNED")

            shipment_status = input("Status: ").strip().upper()

            payment_service.update_shipment(
                shipment_id,
                shipment_status
            )

        elif choice == "7":

            shipment_id = int(input("Shipment ID: "))
            payment_service.track_shipment(shipment_id)

        elif choice == "8":

            payment_service.delivery_status()

        elif choice == "0":

            payment_service.close_session()
            break

        else:

            print("Invalid choice.")
def handle_reports_menu():

    while True:

        print("\n--- Reports & Analytics ---")
        print("1. Monthly Sales Report")
        print("2. Best Selling Products")
        print("3. Customer Purchase History")
        print("4. Pending Orders")
        print("5. Revenue by Category")
        print("6. Low Stock Products")
        print("0. Back")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            report = monthly_sales_report()

            if not report:
                print("No records found.")
            else:
                for row in report:
                    print(row)

        elif choice == "2":

            report = best_selling_products()

            if not report:
                print("No records found.")
            else:
                for row in report:
                    print(row)

        elif choice == "3":

            customer_id = int(input("Customer ID: "))

            report = customer_purchase_history(customer_id)

            print(report)

        elif choice == "4":

            report = pending_orders()

            if not report:
                print("No records found.")
            else:
                for row in report:
                    print(row)

        elif choice == "5":

            report = revenue_by_category()

            if not report:
                print("No records found.")
            else:
                for row in report:
                    print(row)

        elif choice == "6":

            report = low_stock_products_report()

            if not report:
                print("No records found.")
            else:
                for row in report:
                    print(row)

        elif choice == "0":
            break

        else:
            print("Invalid choice.")
def main():
    # Create database tables (only after models are imported)
    try:
        init_db()
    except Exception:
        # Ignore if models are not ready yet
        pass

    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            customer_menu()

        elif choice == "2":
            handle_product_menu()

        elif choice == "3":
            handle_inventory_menu()

        elif choice == "4":
            handle_cart_order_menu()

        elif choice == "5":
            handle_payment_shipment_menu()

        elif choice == "6":
            handle_reports_menu()

        elif choice == "0":
            print("\nThank you for using the system.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()