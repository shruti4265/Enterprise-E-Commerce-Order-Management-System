"""
File : product_service.py
Description : Product & Category Service Layer
"""

import logging

from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from models.category_model import Category
from models.product_model import Product
from models.inventory_model import Inventory  # confirm this matches your actual file


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------- ADD CATEGORY ---------------------------- #

def add_category(category_name, category_description=None):
    session = SessionLocal()

    try:
        if not category_name.strip():
            logger.warning("Category name cannot be empty.")
            return "Category name cannot be empty."

        existing = session.query(Category).filter(
            Category.name == category_name
        ).first()

        if existing:
            logger.warning("Category already exists.")
            return "Category already exists."

        category_object = Category(
            name=category_name,
            description=category_description
        )

        session.add(category_object)
        session.commit()
        session.refresh(category_object)

        logger.info("Category Added Successfully.")
        return "Category Added Successfully."

    except SQLAlchemyError as error:
        session.rollback()
        logger.error(error)
        return "Database Error."

    except Exception as error:
        session.rollback()
        logger.error(error)
        return "Unexpected Error."

    finally:
        session.close()


# ---------------------------- VIEW CATEGORIES ---------------------------- #

def view_categories():
    session = SessionLocal()

    try:
        category_list = session.query(Category).all()

        if not category_list:
            logger.warning("No Categories Found.")
            return []

        logger.info("Categories Retrieved Successfully.")
        return category_list

    except SQLAlchemyError as error:
        logger.error(error)
        return []

    finally:
        session.close()


# ---------------------------- UPDATE CATEGORY ---------------------------- #

def update_category(category_id, new_category_name, new_description=None):
    session = SessionLocal()

    try:
        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:
            logger.warning("Category Not Found.")
            return "Category Not Found."

        if not new_category_name.strip():
            logger.warning("Category Name cannot be empty.")
            return "Category Name cannot be empty."

        duplicate = session.query(Category).filter(
            Category.name == new_category_name
        ).first()

        if duplicate and duplicate.category_id != category_id:
            logger.warning("Category already exists.")
            return "Category already exists."

        category_object.name = new_category_name
        category_object.description = new_description

        session.commit()
        session.refresh(category_object)

        logger.info("Category Updated Successfully.")
        return "Category Updated Successfully."

    except SQLAlchemyError as error:
        session.rollback()
        logger.error(error)
        return "Database Error."

    except Exception as error:
        session.rollback()
        logger.error(error)
        return "Unexpected Error."

    finally:
        session.close()


# ---------------------------- DELETE CATEGORY ---------------------------- #

def delete_category(category_id):
    session = SessionLocal()

    try:
        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:
            logger.warning("Category Not Found.")
            return "Category Not Found."

        if category_object.product_list:
            logger.warning("Category contains products. Delete products first.")
            return "Category contains products. Delete products first."

        session.delete(category_object)
        session.commit()

        logger.info("Category Deleted Successfully.")
        return "Category Deleted Successfully."

    except SQLAlchemyError as error:
        session.rollback()
        logger.error(error)
        return "Database Error."

    except Exception as error:
        session.rollback()
        logger.error(error)
        return "Unexpected Error."

    finally:
        session.close()


# ---------------------------- ADD PRODUCT ---------------------------- #

def add_product(
        product_name,
        product_description,
        product_price,
        initial_quantity,
        is_active,
        category_id,
        low_stock_threshold=10
):
    """
    Add Product + create its matching Inventory row.
    """

    session = SessionLocal()

    try:
        if product_name is None or not str(product_name).strip():
            logger.warning("Product Name cannot be empty.")
            return "Product Name cannot be empty."

        if product_price <= 0:
            logger.warning("Invalid Product Price.")
            return "Product Price must be greater than zero."

        if initial_quantity < 0:
            logger.warning("Invalid Quantity.")
            return "Quantity cannot be negative."

        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:
            logger.warning("Category Not Found.")
            return "Category Not Found."

        duplicate_product = session.query(Product).filter(
            Product.name == product_name,
            Product.category_id == category_id
        ).first()

        if duplicate_product:
            logger.warning("Product already exists.")
            return "Product already exists."

        product_object = Product(
            name=product_name,
            description=product_description,
            price=product_price,
            is_active=is_active,
            category_id=category_id
        )

        session.add(product_object)
        session.flush()  # get product_id before commit, for the Inventory row

        inventory_object = Inventory(
            product_id=product_object.product_id,
            quantity=initial_quantity,
            low_stock_threshold=low_stock_threshold
        )

        session.add(inventory_object)
        session.commit()
        session.refresh(product_object)

        logger.info("Product Added Successfully.")
        return "Product Added Successfully."

    except SQLAlchemyError as error:
        session.rollback()
        logger.error(error)
        return "Database Error."

    except Exception as error:
        session.rollback()
        logger.error(error)
        return "Unexpected Error."

    finally:
        session.close()


# ---------------------------- UPDATE PRODUCT ---------------------------- #

def update_product(
        product_id,
        product_name,
        product_description,
        product_price,
        is_active,
        category_id
):
    """
    Update Product. Stock is NOT touched here — use the Inventory module for that.
    """

    session = SessionLocal()

    try:
        product_object = session.query(Product).filter(
            Product.product_id == product_id
        ).first()

        if product_object is None:
            logger.warning("Product Not Found.")
            return "Product Not Found."

        if product_name is None or not str(product_name).strip():
            logger.warning("Product Name cannot be empty.")
            return "Product Name cannot be empty."

        if product_price <= 0:
            logger.warning("Invalid Product Price.")
            return "Product Price must be greater than zero."

        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:
            logger.warning("Category Not Found.")
            return "Category Not Found."

        duplicate_product = session.query(Product).filter(
            Product.name == product_name,
            Product.category_id == category_id,
            Product.product_id != product_id
        ).first()

        if duplicate_product:
            logger.warning("Product already exists.")
            return "Product already exists."

        product_object.name = product_name
        product_object.description = product_description
        product_object.price = product_price
        product_object.is_active = is_active
        product_object.category_id = category_id

        session.commit()
        session.refresh(product_object)

        logger.info("Product Updated Successfully.")
        return "Product Updated Successfully."

    except SQLAlchemyError as error:
        session.rollback()
        logger.error(error)
        return "Database Error."

    except Exception as error:
        session.rollback()
        logger.error(error)
        return "Unexpected Error."

    finally:
        session.close()


# ---------------------------- DELETE PRODUCT ---------------------------- #

def delete_product(product_id):
    session = SessionLocal()

    try:
        product_object = session.query(Product).filter(
            Product.product_id == product_id
        ).first()

        if product_object is None:
            logger.warning("Product Not Found.")
            return "Product Not Found."

        session.delete(product_object)  # inventory row cascades via ON DELETE CASCADE
        session.commit()

        logger.info("Product Deleted Successfully.")
        return "Product Deleted Successfully."

    except SQLAlchemyError as error:
        session.rollback()
        logger.error(error)
        return "Database Error."

    except Exception as error:
        session.rollback()
        logger.error(error)
        return "Unexpected Error."

    finally:
        session.close()


# ---------------------------- VIEW PRODUCT ---------------------------- #

def view_product(product_id):
    session = SessionLocal()

    try:
        product_object = session.query(Product).filter(
            Product.product_id == product_id
        ).first()

        if product_object is None:
            logger.warning("Product Not Found.")
            return None

        logger.info("Product Retrieved Successfully.")
        return product_object

    except SQLAlchemyError as error:
        logger.error(error)
        return None

    finally:
        session.close()


# ---------------------------- VIEW ALL PRODUCTS ---------------------------- #

def view_all_products():
    session = SessionLocal()

    try:
        product_list = session.query(Product).all()

        if not product_list:
            logger.warning("No Products Found.")
            return []

        logger.info("Products Retrieved Successfully.")
        return product_list

    except SQLAlchemyError as error:
        logger.error(error)
        return []

    finally:
        session.close()


# ---------------------------- SEARCH PRODUCT ---------------------------- #

def search_product(search_value):
    session = SessionLocal()

    try:
        product_list = session.query(Product).filter(
            (Product.name.ilike(f"%{search_value}%")) |
            (Product.product_id == search_value)
        ).all()

        if not product_list:
            logger.warning("Product Not Found.")
            return []

        logger.info("Product Search Successful.")
        return product_list

    except SQLAlchemyError as error:
        logger.error(error)
        return []

    finally:
        session.close()


# ---------------------------- SEARCH BY CATEGORY ---------------------------- #

def search_by_category(category_id):
    session = SessionLocal()

    try:
        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:
            logger.warning("Category Not Found.")
            return []

        product_list = session.query(Product).filter(
            Product.category_id == category_id
        ).all()

        if not product_list:
            logger.warning("No Products Found In This Category.")
            return []

        logger.info("Category Products Retrieved Successfully.")
        return product_list

    except SQLAlchemyError as error:
        logger.error(error)
        return []

    finally:
        session.close()