from services.inventory_service import InventoryService


def inventory_menu():

    inventory_service = InventoryService()

    while True:

        print("\n" + "=" * 50)
        print("         INVENTORY MANAGEMENT SYSTEM")
        print("=" * 50)
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. Update Stock")
        print("4. View Stock")
        print("5. View Inventory")
        print("6. Low Stock Products")
        print("7. Stock History")
        print("8. Exit")
        print("=" * 50)

        try:

            choice = int(input("Enter your choice : "))

            if choice == 1:

                product_id = int(input("Enter Product ID : "))
                quantity = int(input("Enter Quantity to Add : "))
                reason = input("Enter Reason (Press Enter for default) : ").strip()

                if reason:
                    inventory_service.add_stock(
                        product_id,
                        quantity,
                        reason
                    )
                else:
                    inventory_service.add_stock(
                        product_id,
                        quantity
                    )

            elif choice == 2:

                product_id = int(input("Enter Product ID : "))
                quantity = int(input("Enter Quantity to Remove : "))
                reason = input("Enter Reason (Press Enter for default) : ").strip()

                if reason:
                    inventory_service.remove_stock(
                        product_id,
                        quantity,
                        reason
                    )
                else:
                    inventory_service.remove_stock(
                        product_id,
                        quantity
                    )

            elif choice == 3:

                product_id = int(input("Enter Product ID : "))
                quantity = int(input("Enter Updated Quantity : "))
                reason = input("Enter Reason (Press Enter for default) : ").strip()

                if reason:
                    inventory_service.update_stock(
                        product_id,
                        quantity,
                        reason
                    )
                else:
                    inventory_service.update_stock(
                        product_id,
                        quantity
                    )

            elif choice == 4:

                product_id = int(input("Enter Product ID : "))

                inventory_service.view_stock(
                    product_id
                )

            elif choice == 5:

                inventory_service.view_inventory()

            elif choice == 6:

                inventory_service.low_stock_products()

            elif choice == 7:

                print("\n1. View All History")
                print("2. View Product History")

                option = int(input("Choose Option : "))

                if option == 1:

                    inventory_service.stock_history()

                elif option == 2:

                    product_id = int(
                        input("Enter Product ID : ")
                    )

                    inventory_service.stock_history(
                        product_id
                    )

                else:

                    print("Invalid Option.")

            elif choice == 8:

                inventory_service.close_session()

                print("\nThank You!")

                break

            else:

                print("Invalid Choice.")

        except ValueError:

            print("Please enter valid numeric values.")

        except Exception as error:

            print("Error :", error)


if __name__ == "__main__":
    inventory_menu()