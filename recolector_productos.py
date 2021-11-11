import datos
import time
import requests
from bs4 import BeautifulSoup

def insertar_producto(entity):
    con =  datos.sql_connection()
    cursorobj = con.execute("INSERT INTO producto(codigobarra, descripcion, marca, imagen1) VALUES (?, ?, ?, ?)",[entity['codigobarra'], entity['descripcion'], entity['marca'], entity['imagen1']])
    con.commit()
    con.close()

def recorrer_enlaces_productos(enlace):
    req = requests.get(enlace)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        capturar_detalles_producto(soup)
        soup.clear()
    else:
        print('Error al ingresar al enlace del producto')

def capturar_detalles_producto(html_parseado):
    #TODO validar que todo lo buscado se encuentre y en caso de no encontrarse tratar el error
    codigobarra = html_parseado.find('div', attrs={'class': 'sku', 'itemprop': 'sku'}).string
    descripcion = html_parseado.find('h1', attrs={'class': 'productname', 'itemprop':'name'}).string
    try:
        marca = html_parseado.find('div', attrs={'class': 'manufacturers'}).a.string
    except:
        print("sin marca")
        marca = ""
    imagen1 = html_parseado.find('div', attrs={'class': 'ubislider-image-container left'}).find_next('img')['src']
    arreglo = {
        "codigobarra": codigobarra,
        "descripcion": descripcion,
        "marca": marca,
        "imagen1": imagen1
    }
    insertar_producto(arreglo)
    print(arreglo['descripcion'])
    time.sleep(0.123)

con = datos.sql_connection()
for row in datos.obtener_enlaces_productos(con,50000):
    recorrer_enlaces_productos(row[3])
