import time
import datetime
import sqlite3
import controller
import products_controller
import colorama

from controller import clear
from selling_section import selling_section


# Enable Terminal Colorization in the terminal.
colorama.init()


def main():
    '''
    Default section of POS System where all kinds of features resides in.
    This is like the ui for the system for you to interact with.
    '''
    clear()
    print(f"Date: {datetime.datetime.now()}")
    if controller.get_item_list_size() <= 0:
        print("There is no item on the list.")
    else:
        print(controller.get_item_list())
    print("1. Selling Section")
    print("2. Search Products")
    print("3. Add Products")
    print("4. Update Product")
    print("5. Delete Product")
    print("-----------")
    print("6. Logout")
    try:
        answer = int(input("Option -> "))
        if answer == 1:
            selling_section()
        elif answer == 2:
            products_controller.search_products()
        elif answer == 3:
            products_controller.add_product()
        elif answer == 4:
            products_controller.update_product()
        elif answer == 5:
            products_controller.delete_product()
        else:
            print(controller.error_message("%s is not an option." % answer))
            time.sleep(1.5)
            main()
    except ValueError:
        print(controller.error_message("Any kind of alphabets are not allowed, only the numbers are."))
        time.sleep(1.5)
        main()
    except KeyboardInterrupt:
        clear()
        controller.bye_message()
        time.sleep(1.5)
        clear()
        exit(0)


if __name__ == "__main__":
    if controller.create_configuration() == True:
        controller.con = sqlite3.connect("./pos.db")
        main()
    else:
        main()
