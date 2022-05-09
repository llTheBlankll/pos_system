import time
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
            # Change to True because all the check list are satisfied.
            input_valid = True
            
        if input_valid == True:
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
            If there is one, then we will print an info. message that, there can only be one product code in the database.
            '''
            print(controller.info_message(f"{cur.rowcount} rows affected."))
            if cur.rowcount <= 0:
                print(controller.info_message(""))
            else:
                controller.con.commit()
        else:
            print(controller.error_message("I don't know how you passed the screening processed but " +
                                           "this is how far you can belong to."))
            time.sleep(1.5)
            add_product()
    except ValueError as e:
        print(f"ERROR: {controller.error_message(e)}")
        time.sleep(1.5)
        add_product()
    except KeyboardInterrupt:
        print(controller.info_message("\nGoing back to dashboard..."))
        time.sleep(1.5)
        pos_system.main()


def delete_product():
    if no_items_in_list() == True:
        print(controller.info_message("To delete a product, you need to add some first."))
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
    print(controller.search_product(description=description))