from tkinter import * 
from tkinter import messagebox
import sqlite3
import requests
import datetime
import sys


class App():
    pass
class LabelFrame(App):
    pass
class EntryFrame(App):
    pass
class Buttons(App):
    pass
class Cancel(Buttons):
    pass
class Submit(Buttons):
    pass
class Exit(Buttons):
    pass
class Venta():
    def __init__(self, client, cs, cd, ct, dessert):
        price = self.dollar_quote()
        total = self.total_sale(price, cs, cd, ct, dessert)
        self.submit_sale(client,cs,cd,ct,dessert, total)

    def dollar_quote():
        """
        Summary: 
            I use an API that returns the price of the dollar in Argentina.
        Args:
            price: I get in real time the value of the dollar-ARS price
        """
        try:
            r = requests.get("https://api-dolar-argentina.herokuapp.com/api/dolaroficial")
            price = r.json()["venta"]
            price = float(price)
            return price
        except:
            messagebox.showerror(title="Error grave", message="Sin internet para cotizar. Terminado")
            sys.exit()
    def total_sale(price: float, cs: int, cd: int, ct: int, p: int):
        cs *= price
        cd *= price
        ct *= price
        p *= price
        total = cs + cd + ct + p
        return total
    def submit_sale(name:str, cs: int, cd: int, ct: int, p: int, total: float):
        today = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        conn = sqlite3.connect("comercio.sqlite")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO ventas VALUES (null,?,?,?,?,?,?,?)", name, today, cs, cd, ct, p, total)
        except sqlite3.OperationalError:
            cursor.execute("""CREATE TABLE ventas 
            ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                fecha TEXT,
                ComboS INT,
                ComboD INT,
                ComboT INT,
                Postre INT,
                total REAL
            )
            """)
            cursor.execute("INSERT INTO ventas VALUES (null,?,?,?,?,?,?,?)", name, today, cs, cd, ct, p, total)
        conn.commit()
        conn.close

if __name__ == "__main__":
    pass