import os
import json
import hashlib
import logging
from datetime import datetime

# Setup paths
BASE_DIR = "data"
os.makedirs(BASE_DIR, exist_ok=True)

CUSTOMERS_JSON = os.path.join(BASE_DIR, "customers.json")
ORDERS_JSON = os.path.join(BASE_DIR, "orders.json")

# Logging Setup
LOG_FILE = os.path.join(BASE_DIR, "brew_and_book.log")
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_and_print(msg, level="info"):
    print(msg)
    if level == "info":
        logging.info(msg)
    elif level == "error":
        logging.error(msg)
    elif level == "debug":
        logging.debug(msg)

# Helper Functions
def sha256(text):
    return hashlib.sha256(text.encode()).hexdigest()

def load_json(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# Customer Functions
def register_customer(email, name, password):
    customers = load_json(CUSTOMERS_JSON)
    if any(c["email"] == email for c in customers):
        return None  # already exists
    customer = {
        "email": email,
        "name": name,
        "password_hash": sha256(password),
        "created_at": datetime.now().isoformat()
    }
    customers.append(customer)
    save_json(CUSTOMERS_JSON, customers)
    log_and_print(f"Customer {name} registered successfully!", "info")
    return customer

def login_customer(email, password):
    customers = load_json(CUSTOMERS_JSON)
    for c in customers:
        if c["email"] == email and c["password_hash"] == sha256(password):
            log_and_print(f"Customer {c['name']} logged in!", "info")
            return c
    return None

# Menu with Prices + Descriptions
MENU = {
    "Food": {
        "Sandwich": {"price": 5, "desc": "Freshly made sandwich with veggies and cheese"},
        "Pasta": {"price": 8, "desc": "Italian pasta with rich tomato sauce"},
        "Salad": {"price": 6, "desc": "Healthy green salad with dressing"}
    },
    "Beverages": {
        "Coffee": {"price": 3, "desc": "Hot brewed coffee"},
        "Tea": {"price": 2, "desc": "Refreshing green tea"},
        "Juice": {"price": 4, "desc": "Fresh fruit juice"}
    },
    "Cafe Specials": {
        "Cheesecake": {"price": 4, "desc": "Creamy baked cheesecake with berries"},
        "Muffins": {"price": 3, "desc": "Soft chocolate chip muffins"},
        "Croissants": {"price": 3, "desc": "Buttery French croissants"}
    },
    "Books": {
        "The Alchemist": {"price": 10, "desc": "Paulo Coelho's inspirational novel"},
        "1984": {"price": 12, "desc": "George Orwell’s dystopian classic"},
        "Harry Potter": {"price": 15, "desc": "Magical fantasy novel by J.K. Rowling"},
        "Atomic Habits": {"price": 14, "desc": "James Clear’s guide to building good habits"}
    }
}

# Menu & Orders
def menu_page(cart):
    while True:
        print("\n=== Brew N Book Menu ===")
        for i, category in enumerate(MENU.keys(), 1):
            print(f"{i}) {category}")
        print(f"{len(MENU)+1}) Proceed to Checkout")
        print(f"{len(MENU)+2}) Exit")

        choice = input("Select option: ").strip()
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(MENU):
                category = list(MENU.keys())[choice - 1]
                add_to_cart(cart, category, MENU[category])
            elif choice == len(MENU) + 1:
                return  # checkout
            elif choice == len(MENU) + 2:
                exit()
            else:
                log_and_print("Invalid menu choice!", "error")
        else:
            log_and_print("Invalid input!", "error")

def add_to_cart(cart, category, items):
    print(f"\n=== {category} Menu ===")
    item_list = list(items.items())
    for i, (item, info) in enumerate(item_list, 1):
        print(f"{i}) {item} - €{info['price']} | {info['desc']}")

    choice = input("Select item number (or press Enter to go back): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(item_list):
        item, info = item_list[int(choice) - 1]

        # Ask for quantity in pieces
        qty = input(f"How many pieces of {item} would you like? ").strip()
        if not qty.isdigit() or int(qty) <= 0:
            log_and_print("Invalid quantity. Defaulting to 1.", "error")
            qty = 1
        else:
            qty = int(qty)

        total_price = info['price'] * qty
        cart.append({
            "category": category,
            "item": item,
            "price": info['price'],
            "quantity": qty,
            "subtotal": total_price,
            "desc": info['desc']
        })
        log_and_print(f"Added {qty} x {item} (€{total_price}) to cart", "info")
    else:
        log_and_print("No valid item selected, returning to menu.", "debug")

# Checkout Process
def checkout(cart):
    if not cart:
        log_and_print("Cart is empty. Nothing to checkout.", "error")
        return

    print("\n=== Checkout ===")
    total = 0
    for i, item in enumerate(cart, 1):
        print(f"{i}) {item['item']} ({item['category']}) x{item['quantity']} - €{item['subtotal']}")
        total += item['subtotal']
    print(f"\nTotal Amount: €{total}")

    # Customer login/register
    email = input("Enter email: ").strip().lower()
    password = input("Enter password: ").strip()

    customer = login_customer(email, password)
    if not customer:
        print("No account found. Creating new account...")
        name = input("Enter your name: ").strip()
        customer = register_customer(email, name, password)
        if not customer:
            log_and_print("Registration failed. Checkout aborted.", "error")
            return

    # Collect delivery and payment details
    address = input("Enter delivery address: ").strip()
    payment = input("Payment method (Cash/Card): ").strip().capitalize()
    notes = input("Additional notes (optional): ").strip()

    # Generate unique order ID
    order_id = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Save order
    orders = load_json(ORDERS_JSON)
    orders.append({
        "order_id": order_id,
        "customer_email": customer["email"],
        "customer_name": customer["name"],
        "items": cart,
        "address": address,
        "payment": payment,
        "notes": notes,
        "total_amount": total,
        "timestamp": datetime.now().isoformat()
    })
    save_json(ORDERS_JSON, orders)
    log_and_print(f"Order {order_id} placed successfully for {customer['name']} - Total €{total}", "info")

    # Order summary
    print("\n=== Final Order Summary ===")
    print(f"Order ID: {order_id}")
    for i, item in enumerate(cart, 1):
        print(f"{i}) {item['item']} x{item['quantity']} - €{item['subtotal']}")
    print(f"Total to Pay: €{total}")
    print(f"Address: {address}")
    print(f"Payment: {payment}")
    if notes:
        print(f"Notes: {notes}")
    print("Thank you for ordering with Brew N Book!")

# Front Page
def front_page():
    while True:
        print("\n=== Welcome to Brews N Books ===")
        print("1) Menu ")
        print("2) Employee Login")
        print("3) Exit")

        choice = input("Select option: ").strip()
        if choice == "1":
            cart = []
            menu_page(cart)
            checkout(cart)

        elif choice == "2":
            # Employee login placeholder
            print("\n=== Employee Login ===")
            email = input("Enter employee email: ").strip().lower()
            password = input("Enter password: ").strip()

            if email == "admin@brew.com" and password == "admin123":
                print("Employee logged in successfully!")
                print("Employee functions (discounts, stock management, etc.) will be added later.")
            else:
                print("Invalid employee credentials. Access denied.")

        elif choice == "3":
            log_and_print("Program exited.", "info")
            break
        else:
            log_and_print("Invalid option on front page!", "error")

# Main Program
if __name__ == "__main__":
    front_page()
