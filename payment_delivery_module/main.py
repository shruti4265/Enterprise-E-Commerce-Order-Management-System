"""
main.py

Entry point for the Payment & Shipment Module.
"""

from database_initializer import init_db
from payment_menu import payment_menu


def display_menu():
    print("\n" + "=" * 60)
    print("         PAYMENT & SHIPMENT MANAGEMENT")
    print("=" * 60)
    print("1. Payment Management")
    print("2. Shipment Management")
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
            payment_menu("payment")

        elif choice == "2":
            payment_menu("shipment")

        elif choice == "0":
            print("\nThank you for using the system.")
            break

        else:
            print("\nInvalid choice. Please try again.")


if __name__ == "__main__":
    main()