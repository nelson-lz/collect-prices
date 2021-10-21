import time
import json
import requests
from bs4 import BeautifulSoup

PAGE_INDEX ="?pageindex="
url = "https://www.stock.com.py/default.aspx"
enlaces_categorias = {}
enlaces_categorias['links']= []
enlaces_productos = {}
enlaces_productos['enlace_producto'] = []

def recorrer_pagina_categoria(link_cateogrie):

    for i in range(50):
        req = requests.get(link_cateogrie+PAGE_INDEX+(str(i+1)))
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            try:
                #en este primer paginado siempre hay productos
                recolectar_links_productos(soup)
                #aqui verificamos si ha terminado de hacer el paginado, en caso de que ya no
                #exista mas los botones del paginado ha terminado
                soup.find('div', attrs={'class': 'product-pager-box'}).div.a
                print("paginando... " + str(i + 1))
            except:
                print("error en el paginado jeje opa el paginado")
                break
        else:
            print("Error en el recorrido de las categorias")
    time.sleep(0.125)


def recolectar_links_productos(html_parseado):
    for elem in html_parseado.find_all('div', attrs={'class': 'product-item'}):
        arreglo_json= {
            "producto":elem.h2.a.string,
            "link":elem.h2.a['href']
        }
        enlaces_productos['enlace_producto'].append(arreglo_json)
        # e1 = enl.Enlace(elem.h2.a.string, elem.h2.a['href'])
        # enlaces_productos.append(e1)

#escribir en archivo json
def guardar_en_json(nombre_archivo, diccionario):
    try:
        with open(nombre_archivo, "w") as archivo_json:
            # escribimos y especificamos la identacion 4 espacios en este caso
            #archivo_json.write(json.dump(diccionario, indent=4))
            json.dump(diccionario,archivo_json, indent=4)
    except:
        print("Error al escribir el arhivo_json")

req = requests.get(url)
#recolectamos los links de las categorias de productos para luego
# recorrerlos por cada pagina y recolectar los links de los productos
if req.status_code == 200:
    soup = BeautifulSoup(req.text,'html.parser')
    for elem in soup.find_all('li',attrs={'class':'level3'}):
        arrreglo_json = {
            'categoria': elem.a.string,
            'link' : elem.a['href']
        }
        enlaces_categorias['links'].append(arrreglo_json)

guardar_en_json('categorias.json',enlaces_categorias)
#iteraracion de los links de las categorias y captura links de cada producto
conteo = 0

#El deborador de memoria(se debe dividir el recorrido de las categorias para que no sature la memoria)
#TODO ver como optimizar el uso de recursos
for enlace in enlaces_categorias.values():
    for enl in enlace:
        conteo = conteo + 1
        if conteo > 399:
            recorrer_pagina_categoria(enl['link'])
            # if conteo > 400:
            #     break

guardar_en_json('productos400-620.json',enlaces_productos)

print("Cantidad de categorias:"+str(len(enlaces_categorias)))
print("Cantidad de Productos:"+str(len(enlaces_productos)))