from sqlalchemy import select, or_

from database import get_db_session
from models.customer_model import Customer
from models.address_model import Address

from validations.customer_validation import (
    validate_required_fields,
    validate_email,
    validate_phone,
    check_duplicate_email
)

from exceptions.custom_exception import (
    ValidationError,
    DatabaseError
)

from utilities.logger import get_logger

logger = get_logger(__name__)


def add_customer(customer_name, customer_email, customer_phone):

    try:

        if not validate_required_fields(
            customer_name,
            customer_email,
            customer_phone
        ):
            raise ValidationError("All fields are required.")

        if not validate_email(customer_email):
            raise ValidationError("Invalid email address.")

        if not validate_phone(customer_phone):
            raise ValidationError("Invalid phone number.")

        if check_duplicate_email(customer_email):
            raise ValidationError("Email already exists.")

        customer = Customer(
            customer_name,
            customer_email,
            customer_phone
        )

        with get_db_session() as session:

            session.add(customer)

            logger.info("Customer added successfully.")

            return customer

    except ValidationError:

        logger.error("Customer validation failed.", exc_info=True)
        raise

    except Exception:

        logger.error("Unable to add customer.", exc_info=True)
        raise DatabaseError("Unable to add customer.")


def view_all_customers():

    try:

        with get_db_session() as session:

            statement = select(Customer)

            customer_list = session.scalars(statement).all()

            logger.info("Customer list fetched successfully.")

            return customer_list

    except Exception:

        logger.error(
            "Unable to fetch customers.",
            exc_info=True
        )

        raise DatabaseError("Unable to fetch customers.")
    from sqlalchemy import or_


def view_customer(customer_id):

    try:

        with get_db_session() as session:

            statement = (
                select(Customer)
                .where(Customer.customer_id == customer_id)
            )

            customer = session.scalars(statement).first()

            if customer is None:
                raise ValidationError("Customer not found.")

            logger.info("Customer fetched successfully.")

            return customer

    except ValidationError:

        logger.error("Customer not found.", exc_info=True)
        raise

    except Exception:

        logger.error(
            "Unable to fetch customer.",
            exc_info=True
        )

        raise DatabaseError("Unable to fetch customer.")


def search_customer(search_value):

    try:

        with get_db_session() as session:

            statement = (
                select(Customer)
                .where(
                    or_(
                        Customer.name.ilike(f"%{search_value}%"),
                        Customer.email.ilike(f"%{search_value}%"),
                        Customer.phone.ilike(f"%{search_value}%")
                    )
                )
            )

            customer_list = session.scalars(statement).all()

            logger.info("Customer search completed.")

            return customer_list

    except Exception:

        logger.error(
            "Unable to search customer.",
            exc_info=True
        )

        raise DatabaseError("Unable to search customer.")


def update_customer(customer_id, customer_name, customer_email, customer_phone):

    try:

        if not validate_required_fields(
            customer_name,
            customer_email,
            customer_phone
        ):
            raise ValidationError("All fields are required.")

        if not validate_email(customer_email):
            raise ValidationError("Invalid email address.")

        if not validate_phone(customer_phone):
            raise ValidationError("Invalid phone number.")

        with get_db_session() as session:

            statement = (
                select(Customer)
                .where(Customer.customer_id == customer_id)
            )

            customer = session.scalars(statement).first()

            if customer is None:
                raise ValidationError("Customer not found.")

            customer.name = customer_name
            customer.email = customer_email
            customer.phone = customer_phone

            logger.info("Customer updated successfully.")

            return customer

    except ValidationError:

        logger.error("Customer update failed.", exc_info=True)
        raise

    except Exception:

        logger.error(
            "Unable to update customer.",
            exc_info=True
        )

        raise DatabaseError("Unable to update customer.")


def delete_customer(customer_id):

    try:

        with get_db_session() as session:

            statement = (
                select(Customer)
                .where(Customer.customer_id == customer_id)
            )

            customer = session.scalars(statement).first()

            if customer is None:
                raise ValidationError("Customer not found.")

            session.delete(customer)

            logger.info("Customer deleted successfully.")

            return True

    except ValidationError:

        logger.error("Customer delete failed.", exc_info=True)
        raise

    except Exception:

        logger.error(
            "Unable to delete customer.",
            exc_info=True
        )

        raise DatabaseError("Unable to delete customer.")
    
def add_address(
    customer_id,
    customer_address,
    customer_city,
    customer_state,
    customer_pincode,
    country,
    is_default=False
):

    try:

        with get_db_session() as session:

            statement = select(Customer).where(
                Customer.customer_id == customer_id
            )

            customer = session.scalars(statement).first()

            if customer is None:
                raise ValidationError("Customer not found.")

            address = Address(
                customer_id,
                customer_address,
                customer_city,
                customer_state,
                customer_pincode,
                country,
                is_default
            )

            session.add(address)

            logger.info("Address added successfully.")

            return address

    except ValidationError:

        logger.error("Address validation failed.", exc_info=True)
        raise

    except Exception:

        logger.error("Unable to add address.", exc_info=True)
        raise DatabaseError("Unable to add address.")


def update_address(
    address_id,
    customer_address,
    customer_city,
    customer_state,
    customer_pincode,
    country,
    is_default=False
):

    try:

        with get_db_session() as session:

            statement = select(Address).where(
                Address.address_id == address_id
            )

            address = session.scalars(statement).first()

            if address is None:
                raise ValidationError("Address not found.")

            address.address_line1 = customer_address
            address.city = customer_city
            address.state = customer_state
            address.postal_code = customer_pincode
            address.country = country
            address.is_default = is_default

            logger.info("Address updated successfully.")

            return address

    except ValidationError:

        logger.error("Address update failed.", exc_info=True)
        raise

    except Exception:

        logger.error("Unable to update address.", exc_info=True)
        raise DatabaseError("Unable to update address.")


def delete_address(address_id):

    try:

        with get_db_session() as session:

            statement = select(Address).where(
                Address.address_id == address_id
            )

            address = session.scalars(statement).first()

            if address is None:
                raise ValidationError("Address not found.")

            session.delete(address)

            logger.info("Address deleted successfully.")

            return True

    except ValidationError:

        logger.error("Address delete failed.", exc_info=True)
        raise

    except Exception:

        logger.error("Unable to delete address.", exc_info=True)
        raise DatabaseError("Unable to delete address.")    