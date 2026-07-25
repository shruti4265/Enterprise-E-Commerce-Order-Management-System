# Enterprise E-Commerce Order Management System

A modular e-commerce backend built with Python and SQLAlchemy (MySQL). The
project is split into six functional modules, each owned by a team member,
sharing a common database layer, logger, and exception hierarchy.

## Tech Stack

- Python 3
- SQLAlchemy (ORM)
- PyMySQL (MySQL driver)
- MySQL

## Project Structure

```
.
├── main.py                     # CLI entry point / menu
├── database.py                 # Shared engine, session factory, get_db_session()
├── database_initializer.py     # Creates all tables from the ORM models
├── schema.sql                  # Reference SQL schema
├── requirements.txt
│
├── models/                     # One SQLAlchemy model per table
│   ├── customer_model.py
│   ├── address_model.py
│   ├── category_model.py
│   ├── product_model.py
│   ├── inventory_model.py
│   ├── stock_transaction_model.py
│   ├── cart_model.py
│   ├── cart_item_model.py
│   ├── order_model.py
│   ├── order_item_model.py
│   ├── payment_model.py
│   └── shipment_model.py
│
├── services/                   # Business logic per module
│   ├── customer_service.py
│   ├── product_service.py
│   ├── inventory_service.py
│   ├── order_service.py
│   ├── payment_service.py
│   └── report_service.py
│
├── validations/                # Input validation helpers
│   ├── validation.py            # Inventory validation
│   ├── customer_validation.py   # Customer/email/phone validation
│   └── payment_validation.py    # Payment validation
│
├── exceptions/
│   └── custom_exception.py      # ValidationError, DatabaseError, ApplicationError
│
└── utilities/
    ├── logger.py                 # Shared logger setup
    └── report_generator.py       # Console formatting for reports
```

## Module Ownership

| Module | Owner | Tables |
|---|---|---|
| Customer Management | Member 1 | `customers`, `addresses` |
| Product & Category | Member 2 | `categories`, `products` |
| Inventory | Member 3 | `inventory`, `stock_transactions` |
| Cart & Order | Member 4 | `carts`, `cart_items`, `orders`, `order_items` |
| Payment & Shipment | Member 5 | `payments`, `shipments` |
| Reports & Analytics | Member 6 | (reads across all tables) |

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/shruti4265/Enterprise-E-Commerce-Order-Management-System.git
   cd Enterprise-E-Commerce-Order-Management-System
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   venv\Scripts\activate      # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the database connection**
   Update the MySQL connection details in `database.py` (host, username,
   password, database name) to match your local MySQL setup. Make sure the
   target database already exists in MySQL before continuing:
   ```sql
   CREATE DATABASE ecommerce_order_management;
   ```

5. **Create the tables**
   ```bash
   python database_initializer.py
   ```

6. **Run the app**
   ```bash
   python main.py
   ```

## Working on a Module

- Branch off `main` for any new work — don't `git init` a fresh repo, always
  `git clone` or `git checkout -b <branch-name>` from this one, otherwise
  your branch won't share history with `main` and can't be merged normally.
- Import shared infrastructure instead of recreating it:
  ```python
  from database import Base, get_db_session
  from utilities.logger import get_logger
  from exceptions.custom_exception import ValidationError, DatabaseError
  ```
- Keep new files inside the existing `models/`, `services/`, `validations/`
  folders at the project root — don't create a separate nested project
  folder for your module.

## Status

- ✅ Customer & Address
- ✅ Product & Category
- ✅ Inventory
- ✅ Cart & Order
- ✅ Payment & Shipment
- ✅ Reports & Analytics

All modules have been merged into `main` and the full flow (customer →
product → cart → order → payment → shipment → reports) has been tested
end to end.