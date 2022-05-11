from math import prod
import time
from typing import Dict

from numpy import delete, product
import controller
import pos_system

from controller import clear


def no_items_in_list() -> bool:
    '''
    Check if there is no items in the database.
    
    Returns:
        [False] : If there is an item or more in the database.
        [True]  : Absolutely zero or no item at all in the database.
    '''
    if controller.get_item_list_size() <= 0:
        return True
    else:
        return False


def add_product():
    clear()
    # If all the input the user entered are correct, then this will change to True
    input_valid: bool = False
    print(controller.info_message("Press Ctrl + C to go back to dashboard."))
    print(controller.info_message("Add Products, enter all the required information below."))
    try:
        product_code = int(input("Product Code (numbers only): "))
        product_description = str(input("Product Description: "))
        product_price = int(input("Price: "))
        product_quantity = int(input("Quantity: "))
        if product_code == "":
            print(controller.error_message("Product Code cannot be empty."))
            time.sleep(1.5)
            add_product()
        elif product_description == "":
            print(controller.error_message("Product Description cannot be empty."))
            time.sleep(1.5)
            add_product()
        elif product_price < 0:
            print(controller.error_message("Product Price cannot be negative or below zero."))
            time.sleep(1.5)
            add_product()
        elif product_quantity < 0:
            print(controller.error_message("Product Quantity cannot be negative or below zero."))
            time.sleep(1.5)
            add_product()
        else:
            # Change to True because all the input are all valid values.
            input_valids = True
            
        if input_valids == True:
            cur = controller.sqlite_execute("INSERT INTO item (" +
                                      "item_product_code," +
                                      "item_description," +
                                      "item_price," +
                                      "item_quantity" +
                                      ") VALUES (?, ?, ?, ?)",
                                      (product_code, product_description,
                                        product_price, product_quantity))
            '''
            There cannot be a duplicate of products. We are basing them from the product code,
            we will first check in the database if there is an already existing product code.
            If there is one, then we will print an info message that, every product code must be unique.
            '''
            print(controller.info_message(f"{cur.rowcount} rows affected."))
            if cur.rowcount <= 0:
                print(controller.info_message(""))
            else:
                controller.con.commit()
                print(controller.info_message(f"Product {product_code} successfully inserted."))
                time.sleep(1.5)
                pos_system.main()
        else:
            print(controller.error_message("I don't know how you passed the screening process but " +
                                           "this is how far you can belong to."))
            time.sleep(1.5)
            add_product()
    except ValueError:
        print(f"ERROR: {controller.error_message('Please validate your input. They cannot be blank or you entered a alphabet on a number field')}")
        time.sleep(1.5)
        add_product()
    except KeyboardInterrupt:
        print(controller.info_message("\nGoing back to dashboard..."))
        time.sleep(1.5)
        pos_system.main()


def delete_product():
    clear()
    # If there is no item on the database, then this section is not available like the others (update, search, and delete).
    if no_items_in_list() == True:
        print(controller.info_message("To delete a product, you need to add some first."))
        time.sleep(1.5)
        pos_system.main()

    print(controller.info_message(controller.get_item_list()))
    try:
        product_code = int(input("Product Code: "))
        
        # Print the information about the item by product code
        item: Dict = controller.get_item(product_code)
        # Check if the product code exist in the database.
        if item == None:
            print(controller.error_message(f"No {product_code} Product Code found."))
            time.sleep(1.5)
            delete_product()
        
        print(controller.info_message(f"Item ID: {item['item_id']}\n" +
                                      f"Item Product Code: {item['item_product_code']}\n" +
                                      f"Item Description : {item['item_description']}\n" +
                                      f"Item Price: {item['item_price']}\n" +
                                      f"Item Quantity: {item['item_quantity']}\n"))
        
        confirm = input(f"Are you sure you want to delete {item['item_product_code']}? yes/no: ")
        if confirm.lower() == "yes" or confirm.lower() == "y":
            if controller.delete_product(product_code):
                print(controller.info_message("Item successfully deleted."))
                time.sleep(1)
                pos_system.main()
            else:
                print(controller.error_message("Item was not deleted successfully."))
                time.sleep(1)
                pos_system.main()
        else:
            pos_system.main()
    except ValueError:
        print(controller.error_message("Any kind of alphabets are not allowed, only the numbers are."))
        time.sleep(1.5)
        delete_product()
    except KeyboardInterrupt:
        print(controller.info_message("\nGoing back to dashboard..."))
        time.sleep(1.5)
        pos_system.main()


def update_product():
    if no_items_in_list() == True:
        print(controller.info_message("To update a product, you need to add some first."))
        time.sleep(1.5)
        pos_system.main()


def search_products():
    if no_items_in_list() == True:
        print(controller.info_message("To search products, you need to add some first."))
        time.sleep(1.5)
        pos_system.main()
    
    print(controller.info_message("Search Items"))
    print("Enter possible description below.")
    description = str(input("-> "))
    print(controller.search_product(description))