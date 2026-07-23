"""
payment_menu.py

Payment & Shipment Management Menu
"""

from services.payment_service import PaymentService


payment_service = PaymentService()


def payment_menu(module):

    while True:

        if module == "payment":

            print("\n========== PAYMENT MANAGEMENT ==========")
            print("1. Make Payment")
            print("2. Verify Payment")
            print("3. Payment History")
            print("4. Refund Payment")
            print("0. Back")

            choice = input("Enter your choice: ").strip()

            if choice == "1":

                order_id = int(input("Enter Order ID: "))
                amount = float(input("Enter Payment Amount: "))
                payment_method = input(
                    "Enter Payment Method (UPI/Card/Cash): "
                )

                payment_service.make_payment(
                    order_id,
                    amount,
                    payment_method
                )

            elif choice == "2":

                payment_id = int(
                    input("Enter Payment ID: ")
                )

                payment_service.verify_payment(payment_id)

            elif choice == "3":

                payment_service.payment_history()

            elif choice == "4":

                payment_id = int(
                    input("Enter Payment ID: ")
                )

                payment_service.refund_payment(payment_id)

            elif choice == "0":

                break

            else:

                print("Invalid choice.")

        elif module == "shipment":

            print("\n========== SHIPMENT MANAGEMENT ==========")
            print("1. Create Shipment")
            print("2. Update Shipment")
            print("3. Track Shipment")
            print("4. Delivery Status")
            print("0. Back")

            choice = input("Enter your choice: ").strip()

            if choice == "1":

                order_id = int(input("Enter Order ID: "))
                tracking_number = input(
                    "Enter Tracking Number: "
                )
                courier_name = input(
                    "Enter Courier Name: "
                )

                payment_service.create_shipment(
                    order_id,
                    tracking_number,
                    courier_name
                )

            elif choice == "2":

                shipment_id = int(
                    input("Enter Shipment ID: ")
                )

                shipment_status = input(
                    "Enter Shipment Status: "
                )

                payment_service.update_shipment(
                    shipment_id,
                    shipment_status
                )

            elif choice == "3":

                shipment_id = int(
                    input("Enter Shipment ID: ")
                )

                payment_service.track_shipment(
                    shipment_id
                )

            elif choice == "4":

                payment_service.delivery_status()

            elif choice == "0":

                break

            else:

                print("Invalid choice.")

        else:

            print("Invalid module.")
            break

    payment_service.close_session()