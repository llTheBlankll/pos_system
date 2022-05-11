import sqlite3
import os
import prettytable
import termcolor

from typing import Dict, Tuple

con: sqlite3.Connection = None

def clear():
    """
    Automatically clear the screen of the terminal whether the os are Windows or Linux.
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
        

def info_message(message: str) -> str:
    '''
    Gives information message.
    
    Color: Blue
    Attributes: None
    '''
    return termcolor.colored(message, color="cyan")


def bye_message() -> None:
    print(info_message("Thank you for using our POS System! :)"))

    
def error_message(message: str) -> str:
    '''
    Gives error message.
    
    Color: Red
    Attributes: Bold
    '''
    return termcolor.colored(message, color="red", attrs=["bold"])


def create_configuration():
    """
    If the database already exists then returns True. If not, then it automatically creates it.

    returns:
        [True]: If the database already exists.
    """
    if os.path.exists("./pos.db"):
        return True

    db_cur = con.cursor()
    db_cur.execute("CREATE TABLE item (" +
                   "item_id INTEGER PRIMARY KEY AUTOINCREMENT," +
                   "item_product_code INTEGER," +
                   "item_description TEXT," +
                   "item_price DOUBLE," +
                   "item_quantity INTEGER )")
    db_cur.commit()


def get_item_list() -> str:
    '''
    Get all the items in the database using prettytable for organized reading.
    
    returns:
        (str): Returns the whole table generated from prettytable.
    '''
    cur: sqlite3.Cursor = con.cursor()
    cur.execute("SELECT item_product_code AS 'Product Code', item_description AS 'Description'," +
                "item_price AS 'Price', item_quantity AS 'Quantity' FROM item")
    x = prettytable.from_db_cursor(cur)
    return x


def get_item_list_size() -> int:
    cur: sqlite3.Cursor = con.cursor()
    cur.execute("SELECT COUNT(*) as count FROM item")
    return cur.fetchone()[0]


def sqlite_execute(statement: str, params: Tuple = ()) -> sqlite3.Cursor:
    '''
    This function returns the sqlite Cursor for you to use with.
    This won't delete or update the database unless you use commit() in sqlite3.Connection
    '''
    db_cursor = con.cursor()
    db_cursor.execute
    return db_cursor.execute(statement, params)


def update_product(product_code: int, to_description: str, to_price: int, to_quantity: int):
    pass


def delete_product(product_code: int) -> bool:
    '''
    Delete the data from database by their product code.
    
    Returns [bool]:
        True: If the item was successfully deleted.
        False: The item was not deleted due to unforeseen circumstances.        
    '''
    delete_cursor = sqlite_execute("DELETE FROM item WHERE item_product_code = ?", (product_code,))
    if delete_cursor.rowcount <= 0:
        return False
    
    # Commit changes to the database.
    con.commit()
    return True


def search_product(description: str) -> str:
    '''
    Search the data from the data corresponding to the description given.
    
    This will return str in a format of prettytable.
    '''
    possible_items: sqlite3.Cursor = sqlite_execute("SELECT item_product_code AS 'Item Product Code'," +
                                                    "item_description AS 'Description'," +
                                                    "item_price AS 'Price'," +
                                                    "item_quantity AS 'Quantity' FROM item " +
                                                    f"WHERE item_description LIKE '%{description}%'")
    return prettytable.from_db_cursor(possible_items)


def get_item(product_code: int) -> Dict or None:
    '''
    Get the data from database.
    
    Returns Dictionary below:
    {
        "item_id": int,
        "item_product_code": int,
        "item_description": text/str,
        "item_price": double/float,
        "item_quantity": int
    }
    '''
    cur = sqlite_execute("SELECT * FROM item WHERE item_product_code = ?", (product_code,))
    cur = cur.fetchone()
    
    if cur == None:
        return None
    
    data: Dict = {
        "item_id": int(cur[0]),
        "item_product_code": int(cur[1]),
        "item_description": str(cur[2]),
        "item_price": float(cur[3]),
        "item_quantity": int(cur[4])
    }
    
    return data
    