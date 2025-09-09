import os
import json
import hashlib
import logging
from datetime import datetime
import db_functions
from helpers import save_json, load_json, sha256
from config import MENU, CUSTOMERS_JSON, ORDERS_JSON
from helpers import log_and_print
from employees import employee_login, employee_menu


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


# Menu & Orders
def menu_page(cart):
    while True:
        print("\n=== Brew N Book Menu ===")
        for i, category in enumerate(MENU.keys(), 1):
            print(f"{i}) {category}")
        print(f"{len(MENU)+1}) Proceed to Checkout")
        

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
    # item_list = list(items.items())
    for i, item in enumerate(items, 1):
        print(f"{i}) {item['name']} - €{item['price']} | {item['desc']}")

    choice = input("Select item number (or press Enter to go back): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(items):
        selected = items[int(choice) - 1]

        # Ask for quantity in pieces
        qty = input(f"How many pieces of {selected['name']} would you like? ").strip()
        if not qty.isdigit() or int(qty) <= 0:
            log_and_print("Invalid quantity. Defaulting to 1.", "error")
            qty = 1
        else:
            qty = int(qty)

        total_price = selected['price'] * qty
        cart.append({
            "category": category,
            "item": selected['name'],
            "price": selected['price'],
            "quantity": qty,
            "subtotal": total_price,
            "desc": selected['desc']
        })
        log_and_print(f"Added {qty} x {selected['name']} (€{total_price}) to cart", "info")
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
            if employee_login(email, password):
                employee_menu()
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
