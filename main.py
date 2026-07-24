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
from exceptions.custom_exception import ValidationError, DatabaseError


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
            print("\nProduct Management module will be integrated here.")

        elif choice == "3":
            print("\nInventory Management module will be integrated here.")

        elif choice == "4":
            print("\nCart & Order Management module will be integrated here.")

        elif choice == "5":
            print("\nPayment & Shipment module will be integrated here.")

        elif choice == "6":
            print("\nReports module will be integrated here.")

        elif choice == "0":
            print("\nThank you for using the system.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()