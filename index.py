from tkinter import ttk
from tkinter import *

import sqlite3

class Product:
    # connection dir property
    db_name = 'database.db'

    def __init__(self, window):
        # Initializations 
        self.wind = window
        self.wind.title('Quimica "ElPrimo" ')
        
        #creating a frame inventario
        frame2 = LabelFrame(self.wind, text = 'ventas registradas')
        frame2.grid(row = 1, column = 0)
        
        #venta nombre input 
        Label(frame2, text = 'producto-Vendido: ').grid(row = 1, column = 0)
        self.producto = Entry(frame2)
        self.producto.focus()
        self.producto.grid(row = 1, column = 2)
        
        #venta price input 
        Label(frame2, text = 'Monto-Venta: ').grid(row = 2, column = 0)
        self.ingreso = Entry(frame2)
        self.ingreso.focus()
        self.ingreso.grid(row = 2, column = 2)
        
        # Button registrar venta
        ttk.Button(frame2, text = 'Registrar venta',command=self.add_venta).grid(row = 3,column=1, columnspan = 2, sticky = W + E)
        
        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Registrar nuevo producto')
        frame.grid(row = 1, column = 1, columnspan = 3, pady = 30)

        # Name Input
        Label(frame, text = 'Nombre: ').grid(row = 1, column = 1)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 2)

        # Price Input
        Label(frame, text = 'Precio: ').grid(row = 2, column = 1)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 2)

        # Button Add Product 
        ttk.Button(frame, text = 'Guardar Producto', command = self.add_product).grid(row = 3,column=2, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 1, columnspan = 2, sticky = W + E)

        # Table ventas y egresos
        self.tree2 = ttk.Treeview(height = 10, columns = 1)
        self.tree2.grid(row = 4, column = 0, columnspan = 2)
        self.tree2.heading('#0', text = 'Venta',anchor = CENTER)
        
        #total ingresos
        Label(text = 'Total: ').grid(row = 5, column = 0)
        self.beneficio = Entry(width=10,state="readonly")
        self.beneficio.focus()
        self.beneficio.grid(row = 5, column = 1)

        # Table productos e precios
        self.tree = ttk.Treeview(height = 10, columns = 3)
        self.tree.grid(row = 4, column = 2, columnspan = 2)
        self.tree.heading('#0', text = 'Nombre', anchor = CENTER)
        self.tree.heading('#1', text = 'Precio', anchor = CENTER)

        # Buttons
        ttk.Button(text = 'Borrar', command = self.delete_product).grid(row = 5, column = 3, sticky = W + E)
        ttk.Button(text = 'Editar', command = self.edit_product).grid(row = 5, column = 2, sticky = W + E)

        # Filling the Rows
        self.get_products()
        
        self.get_products2()
        
        

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    
    # Get Products from Database
    def get_products(self):
        # cleaning Table 
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('', 0, text = row[1], values = row[2])
    def get_products2(self):
        # cleaning Table 
        records2 = self.tree2.get_children()
        for element in records2:
            self.tree2.delete(element)
        # getting data
        query2 = 'SELECT * FROM productVendidos ORDER BY producto DESC'
        db_rows2 = self.run_query(query2)
        # filling data
        for row in db_rows2:
            self.tree2.insert('', 0, text = row[1], values = row[2])

    # User Input Validation
    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0
    # User Input Validation2
    def validation2(self):
        return len(self.producto.get()) != 0 and len(self.ingreso.get()) != 0

    def add_product(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?, ?)'
            parameters =  (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Producto {} agregado correctamente..'.format(self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Name and Price is Required'
        self.get_products()
        
    def add_venta(self):
        if self.validation2():
            query2 = 'INSERT INTO productVendidos VALUES(NULL, ?, ?)'
            parameters2 =  (self.producto.get(), self.ingreso.get())
            self.run_query(query2, parameters2)
            self.message['text'] = 'venta de {} registrada correctamente..'.format(self.producto.get())
            self.producto.delete(0, END)
            self.ingreso.delete(0, END)
        else:
            self.message['text'] = 'se requiere un producto y su venta..'
        self.get_products2()

    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record'
            return
        name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit Product'
        # Old Name
        Label(self.edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Price:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old Price 
        Label(self.edit_wind, text = 'Old Price:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'New Name:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_name.get(), name, new_price.get(), old_price)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_name, name, new_price, old_price):
        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        parameters = (new_name, new_price,name, old_price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(name)
        self.get_products()

if __name__ == '__main__':
    window = Tk()
    application = Product(window)
    window.mainloop()