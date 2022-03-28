from tkinter import * 
from tkinter import messagebox
import sqlite3
import requests
from datetime import datetime
import sys


class App():
    def __init__(self, master):
        pass
class LabelFrame(App):
    pass
class EntryFrame(App):
    def __init__(self):
        super().__init__(App)
class Buttons(App):
    def __init__():
        pass
    def borrar_celdas():
        pass
    def ventana_confirmar(self, message: str):
        respuesta = messagebox.askyesno(title="Confirmar" ,message=f"{message}")
        return respuesta
    def cargar_registro(self, encargado: str, operacion: str, caja: float):
        today = datetime.now().strftime("%a %b %d %H:%M:%S %Y")
        conn = sqlite3.connect("comercio.sqlite")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO registro VALUES (null,?,?,?,?)", encargado, today, operacion,caja)
        except sqlite3.OperationalError:
            cursor.execute("""CREATE TABLE registro 
            ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                encargado TEXT,
                fecha TEXT,
                evento TEXT,
                caja REAL
            )
            """)
        cursor.execute("INSERT INTO registro VALUES (null,?,?,?,?)", encargado, today, operacion,caja)
        conn.commit()
        conn.close

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
        self.total = total

    def dollar_quote(self):
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
    def total_sale(self, price: float, cs: int, cd: int, ct: int, p: int):
        cs *= price
        cd *= price
        ct *= price
        p *= price
        total = cs + cd + ct + p
        return total
    def submit_sale(self, name:str, cs: int, cd: int, ct: int, p: int, total: float):
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
    root = Tk()
    root.minsize(800, 600)
    app = App(root)
    root.mainloop()
