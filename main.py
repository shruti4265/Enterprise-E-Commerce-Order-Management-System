"""
main.py

Entry point for the Enterprise E-Commerce Order Management System.
"""

from database_initializer import init_db


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
            print("\nCustomer Management module will be integrated here.")

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