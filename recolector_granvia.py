import datos
from bs4 import BeautifulSoup
import requests
import time
import granvia_list

url = "https://granviaonline.com.py/catalogo"
PAGE_INDEX = "?pageF="
enlaces_categoria = granvia_list.lista_categorias()
enlaces_productos = {}
enlaces_productos['productos'] = []

def recorrer_links_categorias(link_categoria):
    for i in range(50):
        req = requests.get(enlaces_categoria+PAGE_INDEX+(str(i+1)))
        if req.status_code == 200:
            soup = BeautifulSoup(req.text, 'html.parser')
            try:
                #en este primer paginado siempre hay productos
                recolectar_links_productos(soup)
                #aqui verificamos si ha terminado de hacer el paginado, en caso de que ya no
                #exista mas los botones del paginado ha terminado svg-inline--fa fa-frown fa-w-16 fa-2x my-2
                soup.find('svg', attrs={'class': 'svg-inline--fa fa-frown fa-w-16 fa-2x my-2'})
                print("paginando... " + str(i + 1))
            except:
                print("error en el paginado jeje opa el paginado")
                break
        else:
            print("Error en el recorrido de las categorias")
    time.sleep(0.125)

def recolectar_links_productos(html_parseado):
    for elem in html_parseado.find_all('div', attrs={'class': 'product-item'}):
        arreglo_json = {
            "tipo": "producto",
            "descripcion": elem.h2.a.string,
            "link": elem.h2.a['href'],
            "super": "granvia"
        }
        datos.insertar_enlace(arreglo_json)
        enlaces_productos['enlace_producto'].append(arreglo_json)
def capturar_detalles_producto(html_parseado, super):
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
        "imagen1": imagen1,
        "super": super
    }
    datos.insertar_producto(arreglo)
    print(arreglo['descripcion'].split())
def recorrer_enlaces_productos(enlace, super):
    req = requests.get(enlace)
    time.sleep(0.123)
    if req.status_code == 200:
        soup = BeautifulSoup(req.text, 'html.parser')
        capturar_detalles_producto(soup, super)
        soup.clear()
    else:
        print('Error al ingresar al enlace del producto')
def recolectar_productos(con):
    super='granvia'
    for row in datos.obtener_enlaces_productos(con, super, 50000):
        if row[0] > 49250:
            print("Id-del-link: " + str(row[0]))
            recorrer_enlaces_productos(row[3], super)

for enl in enlaces_categoria:
    print(enl)

print("Cantidad de categorias:"+str(len(enlaces_categoria)))
print("Cantidad de Productos:"+str(len(enlaces_productos)))