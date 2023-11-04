from pydantic import FilePath
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, os
from .models import Nota, Producto, Compra, getProductos

# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos de la tienda

productos_collection = tienda_db.productos  # Colección de los productos

#Obtiene productos de la API
#productos = getProductos('https://fakestoreapi.com/products')

#Borra la colección de productos para que no se reinserten los mismos
#productos_collection.drop()

#Inserto los productos de la API en la colección de productos
# for p in productos:

# 	#Se descarga la imagen del producto
# 	url = p["image"]

# 	directorio_destino = "imagenes/"

# 	#Obtiene el nombre original de la imagen
# 	nombre_archivo = os.path.basename(url)

# 	#Crea la ruta del archivo
# 	ruta_archivo_destino = os.path.join(directorio_destino, nombre_archivo)

# 	response = requests.get(url)

# 	#Guarda la imagen en el directorio
# 	with open(ruta_archivo_destino, "wb") as archivo:
# 		archivo.write(response.content)

# 	#Instancia el producto conforme a la clase Producto
# 	product = {
# 		'id_producto': p["id"],
# 		'nombre': p["title"],
# 		'precio': p["price"],
# 		'descripción': p["description"],
# 		'categoría': p["category"],
# 		'imágen': FilePath("imagenes/" + nombre_archivo),
# 		'rating': {'puntuación': p["rating"]["rate"], 'cuenta': p["rating"]["count"]}
# 	}

# 	prod = Producto(**product)
	
# 	#Inserta el producto en la colección de productos
# 	productos_collection.insert_one(prod.model_dump()) 		


# compras_collection = tienda_db.compras  # Colección de las compras realizadas

# #Obtiene las compras de la API
# compras = getProductos('https://fakestoreapi.com/carts')

# #Obtiene los usuarios de la API
# usuarios = getProductos('https://fakestoreapi.com/users')

# #Borra la colección de compras para que no se reinserten las mismas
# compras_collection.drop()

# #Establezco un contador para ir insertando los usuarios en las compras
# user_counter = 0
# for c in compras:
# 	comp = {
# 		'usuario': usuarios[user_counter]["email"],
# 		'fecha': datetime.now(),
# 		'productos': c["products"],
# 	}

# 	compra = Compra(**comp)

# 	#Inserta la compra en la colección de compras
# 	compras_collection.insert_one(compra.model_dump())

# 	user_counter += 1
 
#FUNCTIONS

def GetCategories(productos_collection):
    categories=[]
    for p in productos_collection.find():
        if p["categoría"] not in categories:
            categories.append(p["categoría"])
	
    return categories

def SearchProducts(productos_collection, to_find):
    query = {
        "$or": [
            {"nombre": {"$regex":f"\\b{to_find}\\b", "$options": "i"}},
            {"descripción": {"$regex":f"\\b{to_find}\\b", "$options": "i"}}   
        ]
    }
    
    products = productos_collection.find(query)
    return products
    

def getProductsByCategory(productos_collection, category):
    products = productos_collection.find({"categoría": category})
    return products

def getLastProductID(productos_collection):
    lastID = productos_collection.find_one(sort=[("id_producto", -1)])
    return lastID["id_producto"]
    
#CONSULTAS

def query1(productos_collection):

    consulta1 = {
        "categoría": "electronics",  
        "precio": { "$gte": 100, "$lte": 200 }   
    }

    productos = productos_collection.find(consulta1).sort("precio", 1)

    electronica_ordenada = ""
    for producto in productos:
        electronica_ordenada+=f"{producto}\n\n"
        
    return electronica_ordenada


def query2(productos_collection):
    
    consulta2 = {
        #Soptions: i para que sea case insensitive a mayúsculas y minúsculas
        "descripción": { "$regex": "pocket", "$options": "i" }   
    }

    productos = productos_collection.find(consulta2)

    productos_pocket = ""
    for producto in productos:
        productos_pocket+=f"{producto}\n\n"

    return productos_pocket


def query3(productos_collection):

    consulta3 = {
	    "rating.puntuación": { "$gt": 4 } 
    }

    productos = productos_collection.find(consulta3)

    productos_mayor_4 = ""
    for producto in productos:
        productos_mayor_4+=f"{producto}\n\n"

    return productos_mayor_4


def query4(productos_collection):

    consulta4 = {
	    "categoría": "men's clothing"
    }

    productos = productos_collection.find(consulta4).sort("rating.puntuación", 1)

    ropa_hombre_ordenada = ""
    for producto in productos:
        ropa_hombre_ordenada+=f"{producto}\n\n"

    return ropa_hombre_ordenada


def query5(productos_collection, compras_collection):

    facturacion_total = 0
    for compra in compras_collection.find():
        for producto in compra["productos"]:

            #en el producto que estamos analizando de la compra, obtenemos su respectiva cantidad
            cantidad = producto["quantity"]
            
            #buscamos en la colección de productos el producto que estamos analizando de la compra relacionando el ID
            p = productos_collection.find_one({"id_producto": producto["productId"] })

            #una vez encontrado el producto en la colección de productos, obtenemos su precio
            precio = p["precio"]
            

            facturacion_total += precio * cantidad

    facturacion_total = f"La facturación total es {round(facturacion_total,2)}\n"

    return facturacion_total


def query6(productos_collection, compras_collection):

    facturacion_categoria = {}
    for compra in compras_collection.find():
        for producto in compra["productos"]:

            #en el producto que estamos analizando de la compra, obtenemos su respectiva cantidad
            cantidad = producto["quantity"]

            #buscamos en la colección de productos el producto que estamos analizando de la compra relacionando el ID
            p = productos_collection.find_one({"id_producto": producto["productId"] })

            #una vez encontrado el producto en la colección de productos, obtenemos su precio y su categoría
            precio = p["precio"]
            categoria = p["categoría"]
            
            #si la categoría no está en el diccionario, la añadimos con valor 0, para ir sumando la facturación por categoría
            if categoria not in facturacion_categoria:
                facturacion_categoria[categoria] = 0

            facturacion_categoria[categoria] += precio * cantidad

    facturacion_categoria = f"La facturación por categoría es {facturacion_categoria}"

    return facturacion_categoria
