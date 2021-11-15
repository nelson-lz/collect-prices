import datos
import time
import requests
from bs4 import BeautifulSoup

PAGE_INDEX ="?pageindex="
url = "https://www.superseis.com.py/default.aspx"
enlaces_categorias = {}
enlaces_categorias['links']= []

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
        soup.clear()
    time.sleep(0.125)

def recolectar_links_productos(html_parseado):
    for elem in html_parseado.find_all('div', attrs={'class': 'product-item'}):
        arreglo_json = {
            "tipo": "producto",
            "descripcion": elem.h2.a.string,
            "link": elem.h2.a['href'],
            "super": "super6"
        }
        datos.insertar_enlace(arreglo_json)

#recolectamos los links de las categorias de productos para luego
#recorrerlos por cada pagina y recolectar los links de los productos
def recolectar_links_categorias():
    req = requests.get(url)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        for elem in soup.find_all('li', attrs={'class': 'level3'}):
            arrreglo_json = {
                'tipo': 'categoria',
                'descripcion': elem.a.string,
                'link': elem.a['href'],
                'super': 'super6'
            }
            datos.insertar_enlace(arrreglo_json)
            enlaces_categorias['links'].append(arrreglo_json)
        soup.clear()

#comenzamos a capturar links por categoria
recolectar_links_categorias()
#iteraracion de los links de las categorias y captura links de cada producto
conteo = 0
for enlace in enlaces_categorias.values():
    for enl in enlace:
        conteo = conteo + 1
        if conteo < 700:
            recorrer_pagina_categoria(enl['link'])
        # if conteo > 399:
        #     break

print("Cantidad de categorias:"+str(len(enlaces_categorias)))
