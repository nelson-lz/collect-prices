import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect('stock-super.db')
        return con
        print('Coneccion a la DB con exito.')
    except Error:
        print(Error)

def tabla_de_links(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS enlace(id integer PRIMARY KEY, tipo text, descripcion text, link text)")
    con.commit()
def tabla_productos(con):
    cursorObj = con.cursor()
    cursorObj.execute("CREATE TABLE IF NOT EXISTS producto(id integer PRIMARY KEY, codigobarra text, descripcion text, marca text, imagen1 text)")
    con.commit()
def cerrar_coneccion(con):
    con.close()
def obtener_enlaces_productos(con, limit=50000):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM enlace WHERE tipo = 'producto' LIMIT "+str(limit))
    rows = cursorObj.fetchall()
    return rows

def insertar_enlace(entity):
    con = sql_connection()
    cursorObj = con.execute("INSERT INTO enlace(tipo, descripcion, link, supermercado) VALUES(?,?,?,?)", [entity["tipo"], entity["descripcion"], entity["link"],entity["super"]])
    con.commit()
    con.close()

def insertar_producto(entity):
    con = sql_connection()
    cursorObj =con.execute("INSERT INTO producto(codigobarra, descripcion, marca, imagen1, supermercado) VALUES(?,?,?,?,?)", [entity["codigobarra"], entity["descripcion"], entity["marca"], entity["imagen1"], entity["super"]])
    con.commit()
    con.close()

con = sql_connection()

tabla_de_links(con)
tabla_productos(con)

cerrar_coneccion(con)