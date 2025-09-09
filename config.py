import db_functions
import os
import logging

MENU ={
    "Food:": db_functions.showAllData('food'),
    "Beverages": db_functions.showAllData('drinks'),
    "Cafe Specials":db_functions.showAllData('specials'),
    "Books":db_functions.showAllData('books'),
}


BASE_DIR = "data"
os.makedirs(BASE_DIR, exist_ok=True)

CUSTOMERS_JSON = os.path.join(BASE_DIR, "customers.json")
ORDERS_JSON = os.path.join(BASE_DIR, "orders.json")
EMPLOYEES_JSON = os.path.join(BASE_DIR, "employees.json")

# Logging Setup
LOG_FILE = os.path.join(BASE_DIR, "brew_and_book.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)