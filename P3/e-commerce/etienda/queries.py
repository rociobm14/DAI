from pymongo import MongoClient
from .models import Producto

import logging
logger = logging.getLogger(__name__)

# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos de la tienda

productos_collection = tienda_db.productos  # Colección de los productos

#Functions

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
    
#API
# def get_products():
#     products = productos_collection.find()
#     result = []
#     for p in products:
#         p["id"] = str(p.get("_id"))
#         del p["_id"]
#         p["title"] = p.get("nombre")
#         p["price"] = p.get("precio")
#         p["description"] = p.get("descripción")  
#         p["category"] = p.get("categoría") 
#         p["rating"] = {"rate": p["rating"]["puntuación"], "count": p["rating"]["cuenta"]} 
        
#         result.append(p)
#     return result

# def create_product(producto):
#     try:
#         p = {
#             'id_producto': getLastProductID(productos_collection),
#             'nombre': producto.title,
#             'precio': producto.price,
#             'descripción': producto.description,
#             #'categoría': producto.category,
#             'rating': {'puntuación': producto.rating.rate, 'cuenta': producto.rating.count}
#         }
        
#         product = Producto(**p)
#         productos_collection.insert_one(product.dict())
#         get_products()
    
#     except Exception as e:
#         logger.error(e)
#         logger.info("the product could not be created")
    

#Queries

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
