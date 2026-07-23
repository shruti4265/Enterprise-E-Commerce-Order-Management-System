"""
File : product_service.py
Description : Product & Category Service Layer
"""

import logging

from sqlalchemy.exc import SQLAlchemyError

from database import SessionLocal
from models.category_model import Category
from models.product_model import Product


# ---------------------------- LOGGER ---------------------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------- ADD CATEGORY ---------------------------- #

def add_category(category_name):
    """
    Add New Category
    """

    session = SessionLocal()

    try:

        if not category_name.strip():
            logger.warning("Category name cannot be empty.")
            return "Category name cannot be empty."

        category_object = session.query(Category).filter(
            Category.category_name == category_name
        ).first()

        if category_object:
            logger.warning("Category already exists.")
            return "Category already exists."

        category_object = Category(
            category_name=category_name
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


# ---------------------------- VIEW CATEGORY ---------------------------- #

def view_categories():
    """
    View All Categories
    """

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

def update_category(category_id, new_category_name):
    """
    Update Category
    """

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

        duplicate_category = session.query(Category).filter(
            Category.category_name == new_category_name
        ).first()

        if duplicate_category and duplicate_category.category_id != category_id:

            logger.warning("Category already exists.")

            return "Category already exists."

        category_object.category_name = new_category_name

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
    """
    Delete Category
    """

    session = SessionLocal()

    try:

        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:

            logger.warning("Category Not Found.")

            return "Category Not Found."

        if category_object.product_list:

            logger.warning(
                "Category contains products. Delete products first."
            )

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
        product_quantity,
        product_status,
        category_id
):
    """
    Add Product
    """

    session = SessionLocal()

    try:

        # ---------------- Validation ---------------- #

        if product_name is None or not str(product_name).strip():

            logger.warning("Product Name cannot be empty.")

            return "Product Name cannot be empty."

        if product_price <= 0:

            logger.warning("Invalid Product Price.")

            return "Product Price must be greater than zero."

        if product_quantity < 0:

            logger.warning("Invalid Product Quantity.")

            return "Product Quantity cannot be negative."

        if product_status is None or not str(product_status).strip():

            logger.warning("Product Status cannot be empty.")

            return "Product Status cannot be empty."

        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:

            logger.warning("Category Not Found.")

            return "Category Not Found."

        duplicate_product = session.query(Product).filter(
            Product.product_name == product_name,
            Product.category_id == category_id
        ).first()

        if duplicate_product:

            logger.warning("Product already exists.")

            return "Product already exists."

        # ---------------- Create Object ---------------- #

        product_object = Product(

            product_name=product_name,

            product_description=product_description,

            product_price=product_price,

            product_quantity=product_quantity,

            product_status=product_status,

            category_id=category_id

        )

        session.add(product_object)

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
        product_quantity,
        product_status,
        category_id
):
    """
    Update Product
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

        if product_quantity < 0:

            logger.warning("Product Quantity cannot be negative.")

            return "Product Quantity cannot be negative."

        if product_status is None or not str(product_status).strip():

            logger.warning("Product Status cannot be empty.")

            return "Product Status cannot be empty."

        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:

            logger.warning("Category Not Found.")

            return "Category Not Found."

        duplicate_product = session.query(Product).filter(
            Product.product_name == product_name,
            Product.category_id == category_id,
            Product.product_id != product_id
        ).first()

        if duplicate_product:

            logger.warning("Product already exists.")

            return "Product already exists."

        product_object.product_name = product_name
        product_object.product_description = product_description
        product_object.product_price = product_price
        product_object.product_quantity = product_quantity
        product_object.product_status = product_status
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
    """
    Delete Product
    """

    session = SessionLocal()

    try:

        product_object = session.query(Product).filter(
            Product.product_id == product_id
        ).first()

        if product_object is None:

            logger.warning("Product Not Found.")

            return "Product Not Found."

        session.delete(product_object)

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
    """
    View Product By ID
    """

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

    except Exception as error:

        logger.error(error)

        return None

    finally:

        session.close()
        
        
# ---------------------------- VIEW ALL PRODUCTS ---------------------------- #

def view_all_products():
    """
    View All Products
    """

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

    except Exception as error:

        logger.error(error)

        return []

    finally:

        session.close()


# ---------------------------- SEARCH PRODUCT ---------------------------- #

def search_product(search_value):
    """
    Search Product By ID or Name
    """

    session = SessionLocal()

    try:

        product_list = session.query(Product).filter(
            (Product.product_name.ilike(f"%{search_value}%")) |
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

    except Exception as error:

        logger.error(error)

        return []

    finally:

        session.close()


# ---------------------------- SEARCH BY CATEGORY ---------------------------- #

def search_by_category(category_id):
    """
    View Products By Category
    """

    session = SessionLocal()

    try:

        category_object = session.query(Category).filter(
            Category.category_id == category_id
        ).first()

        if category_object is None:

            logger.warning("Category Not Found.")

            return []

        product_list = session.query(Product).join(Category).filter(
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

    except Exception as error:

        logger.error(error)

        return []

    finally:

        session.close()