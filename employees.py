import db_functions
from helpers import log_and_print
from config import MENU

def employee_login(email, password):
    employees = db_functions.showAllData('employees')
    for e in employees:
        if e["email"] == email and e["password"] == password:
          log_and_print(f"Employee {e['email']} logged in!", "info")
          return e
    return None

def add_edit_menu(option):
   while True:
      if option=='add':print("\n=== Add items ===")
      else: print("\n=== Edit items ===")
      print("1) Books ")
      print("2) Cafe specials ")
      print("3) Beverages")
      print("4) Exit")
      choice = input("Select option: ").strip()
      if choice == "4":
         break
      elif choice == "1":
         obj = add_inputs()
         if(option=="add"):db_functions.addData("books",obj)
         else:
            filter_list = filter_inputs()
            db_functions.updateData("books", filter_list[0], filter_list[1], obj)
         
      elif choice == "2":
         obj = add_inputs()
         if(option=="add"):db_functions.addData("specials",obj)
         else:
            filter_list = filter_inputs()
            db_functions.updateData("specials", filter_list[0], filter_list[1], obj)
      elif choice == "3":
         obj = add_inputs()
         if(option=="add"):db_functions.addData("drinks",obj)
         else:
            filter_list = filter_inputs()
            db_functions.updateData("drinks", filter_list[0], filter_list[1], obj)

      

def add_inputs():
   name = input("Name: ").strip().lower()
   price= int(input("Price: ").strip().lower())
   desc = input("Description: ").strip().lower()
   return {
      "name":name,
      "price":price,
      "desc":desc
   }

def filter_inputs():
   key = input("Key: ").strip().lower()
   value = input("Value: ").strip().lower()
   return [key, value]

def employee_menu():
   while True:
      print("\n=== Employee Login ===")
      print("1) Add items ")
      print("2) Edit items ")
      print("3) Apply Discount")
      print("4) Exit")
      choice = input("Select option: ").strip()
      if choice =="1":
         add_edit_menu('add')
      elif choice =="2":
         add_edit_menu('edit')
      elif choice =="3":
         discount_menu()
      elif choice=="4":
         break
    
def discount_menu():
   while True:
    print("\n=== Discounts ===")
    order_id = input("Please enter order ID: (press Q to return)")
    if order_id.lower()=='q':
       break
    else:
       order = db_functions.findData('orders',"order_id", order_id)
       if order:
          discount = int(input("what discount do you want to apply in %:"))
          order["total_amount"] = round(order["total_amount"]*(1-discount/100),2)
          new_order = db_functions.updateData('orders', "order_id", order_id, order)
          print(f"Success, new price is {new_order['total_amount']}")
       else:
          print("wrong order ID")



    