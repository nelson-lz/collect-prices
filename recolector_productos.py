import datos
import time
import requests
from bs4 import BeautifulSoup

sin_codbarra = 0
sin_descr = 0
sin_marca = 0
sin_img = 0
def insertar_producto(entity):
    con =  datos.sql_connection()
    cursorobj = con.execute("INSERT INTO producto(codigobarra, descripcion, marca, imagen1) VALUES (?, ?, ?, ?)",[entity['codigobarra'], entity['descripcion'], entity['marca'], entity['imagen1']])
    con.commit()
    con.close()

def recorrer_enlaces_productos(enlace):
    req = requests.get(enlace)
    time.sleep(0.123)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        capturar_detalles_producto(soup)
        soup.clear()
    else:
        print('Error al ingresar al enlace del producto')

def capturar_detalles_producto(html_parseado):
    #TODO validar que todo lo buscado se encuentre y en caso de no encontrarse tratar el error
    try:
        codigobarra = html_parseado.find('div', attrs={'class': 'sku', 'itemprop': 'sku'}).string
    except:
        sin_codbarra =+ 1
        codigobarra = ""
    try:
        descripcion = html_parseado.find('h1', attrs={'class': 'productname', 'itemprop':'name'}).string
    except:
        sin_descr =+ 1
        descripcion = ""
    try:
        marca = html_parseado.find('div', attrs={'class': 'manufacturers'}).a.string
    except:
        sin_marca =+ 1
        marca = ""
    try:
        imagen1 = html_parseado.find('div', attrs={'class': 'ubislider-image-container left'}).find_next('img')['src']
    except:
        sin_img =+ 1
        imagen1 = ""
    arreglo = {
        "codigobarra": codigobarra,
        "descripcion": descripcion,
        "marca": marca,
        "imagen1": imagen1
    }
    insertar_producto(arreglo)
    print(arreglo['descripcion'])

con = datos.sql_connection()
print(time.time())
for row in datos.obtener_enlaces_productos(con,50000):
    if row[0] > 49250:
        print("Id-del-link: " + str(row[0]))
        recorrer_enlaces_productos(row[3])

print("productos sin cod barra: " + str(sin_codbarra))
print("productos sin descripcion: " + str(sin_descr))
print("productos sin marca: " + str(sin_marca))
print("productos sin imagen: " + str(sin_img))