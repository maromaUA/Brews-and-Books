import os
import logging
from datetime import datetime
import helpers


# Setup paths

BASE_DIR = "data"
os.makedirs(BASE_DIR, exist_ok=True)

CUSTOMERS_JSON = os.path.join(BASE_DIR, "customers.json")
EMPLOYEES_JSON = os.path.join(BASE_DIR, "employees.json")
ORDERS_JSON = os.path.join(BASE_DIR, "orders.json")


# Logging Setup

LOG_FILE = os.path.join(BASE_DIR, "brew_and_book_dexter08_09_2025.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(msg, level="info"):
    """Print and log a message"""
    print(msg)
    if level == "info":
        logging.info(msg)
    elif level == "error":
        logging.error(msg)
    elif level == "debug":
        logging.debug(msg)


# Helper Functions




# Customer & Employee Functions

def register_customer():
    print("\n=== Customer Registration ===")
    email = input("Enter email: ").strip().lower()
    name = input("Enter name: ").strip()
    password = input("Enter password: ").strip()

    customers = helpers.load_json(CUSTOMERS_JSON)
    if any(c["email"] == email for c in customers):
        log_and_print("Email already registered!", "error")
        return

    customers.append({
        "email": email,
        "name": name,
        "password_hash": helpers.sha256(password),
        "created_at": datetime.now().isoformat()
    })
    helpers.save_json(CUSTOMERS_JSON, customers)
    log_and_print(f"Customer {name} registered successfully!", "info")
    return {email, name}

def login_customer():
    print("\n=== Customer Login ===")
    email = input("Enter email: ").strip().lower()
    password = input("Enter password: ").strip()

    customers = helpers.load_json(CUSTOMERS_JSON)
    for c in customers:
        if c["email"] == email and c["password_hash"] == helpers.sha256(password):
            log_and_print(f"Customer {c['name']} logged in!", "info")
            menu_page(c["name"])
            return
    log_and_print("Invalid email or password!", "error")

def login_employee():
    print("\n=== Employee Login ===")
    emp_id = input("Enter Employee ID: ").strip()
    password = input("Enter password: ").strip()

    employees = helpers.load_json(EMPLOYEES_JSON)
    for e in employees:
        if e["emp_id"] == emp_id and e["password_hash"] == helpers.sha256(password):
            log_and_print(f"Employee {e['name']} logged in!", "info")
            menu_page(e["name"])
            return
    log_and_print("Invalid Employee ID or password!", "error")


# Menu & Orders

def menu_page(user_name):
    food_menu = ["Sandwich", "Pasta", "Salad"]
    beverages_menu = ["Coffee", "Tea", "Juice"]
    specials_menu = ["Cheesecake", "Muffins", "Croissants"]
    books_menu = ["The Alchemist", "1984", "Harry Potter", "Atomic Habits"]
    while True:
        print(f"\n=== Brew N Book Menu === Welcome {user_name}")
        print("1) Food")
        print("2) Beverages")
        print("3) Cafe Specials")
        print("4) Books")  
        print("5) Logout")

        choice = input("Select option: ").strip()
        log_and_print(f"{user_name} selected menu option: {choice}", "debug")
        if choice == "1":
            order_item(user_name, "Food", food_menu) # pass Food menu to order_item
        elif choice == "2":
            order_item(user_name, "Beverages", beverages_menu) # pass Beverages menu to order_item
        elif choice == "3":
            order_item(user_name, "Cafe Specials", specials_menu) # pass Specials menu to order_item
        elif choice == "4":
            order_item(user_name, "Books", books_menu)  # Pass Books menu to order_item
        elif choice == "5":
            log_and_print(f"{user_name} logged out.", "info")
            break
        else:
            log_and_print("Invalid menu choice!", "error")

def order_item(user_name, category, items):
    print(f"\n=== {category} Menu ===")
    for i, item in enumerate(items, 1):
        print(f"{i}) {item}")

    choice = input("Select item number (or press Enter to go back): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(items):
        item = items[int(choice)-1]
        orders = helpers.load_json(ORDERS_JSON)
        orders.append({
            "user": user_name,
            "category": category,
            "item": item,
            "timestamp": datetime.now().isoformat()
        })
        helpers.save_json(ORDERS_JSON, orders)
        log_and_print(f"{user_name} ordered {item} from {category}", "info")
    else:
        log_and_print("No valid item selected, returning to menu.", "debug")

# Front Page & Login Choice

def front_page():
    while True:
        print("\n=== Welcome to Brew N Book ===")
        print("1) Login")
        print("2) Register")
        print("3) Exit")

        choice = input("Select option: ").strip()
        if choice == "1":
            login_choice_page()
        elif choice == "2":
            register_customer()
        elif choice == "3":
            log_and_print("Program exited.", "info")
            break
        else:
            log_and_print("Invalid option on front page!", "error")

def login_choice_page():
    print("\n=== Login Page ===")
    print("1) Customer Login")
    print("2) Employee Login")
    choice = input("Select option: ").strip()
    if choice == "1":
        login_customer()
    elif choice == "2":
        login_employee()
    else:
        log_and_print("Invalid login option!", "error")


# Main Program

if __name__ == "__main__":
    front_page()
