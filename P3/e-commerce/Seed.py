# Seed.py
from pydantic import BaseModel, FilePath, Field, EmailStr, validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, os, pathlib
import Queries

# https://requests.readthedocs.io/en/latest/
def getProductos(api):
	response = requests.get(api)
	return response.json()
				
# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/

class Nota(BaseModel):
	puntuación: float = Field(ge=0., lt=5.)
	cuenta: int = Field(ge=1)

#Clase para inicializar las entradas en MongoDB			
class Producto(BaseModel):
	_id: Any
	id_producto: int
	nombre: str
	precio: float
	descripción: str
	categoría: str
	imágen: str | None
	rating: Nota

	#Valida que el nombre empiece por mayúscula
	@validator('nombre')
	@classmethod
	def empieza_con_mayuscula(cls, v) -> str:
		if not v[0].isupper():
			raise ValueError("El nombre debe empezar por mayúscula.")
		return v.title()
	

class Rate(BaseModel):
	rate: float = Field(e=0., lt=5.)
	count: int = Field(ge=1)


class Compra(BaseModel):
	_id: Any
	usuario: EmailStr
	fecha: datetime
	productos: list	


# Conexión con la BD				
# https://pymongo.readthedocs.io/en/stable/tutorial.html
client = MongoClient('mongo', 27017)

tienda_db = client.tienda                   # Base de Datos de la tienda

productos_collection = tienda_db.productos  # Colección de los productos

#Obtiene productos de la API
productos = getProductos('https://fakestoreapi.com/products')

#Borra la colección de productos para que no se reinserten los mismos
productos_collection.drop()

#Inserto los productos de la API en la colección de productos
for p in productos:

	#Se descarga la imagen del producto
	url = p["image"]

	directorio_destino = "imagenes/"

	#Obtiene el nombre original de la imagen
	nombre_archivo = os.path.basename(url)

	#Crea la ruta del archivo
	ruta_archivo_destino = os.path.join(directorio_destino, nombre_archivo)

	response = requests.get(url)

	#Guarda la imagen en el directorio
	with open(ruta_archivo_destino, "wb") as archivo:
		archivo.write(response.content)

	#Instancia el producto conforme a la clase Producto
	product = {
		'id_producto': p["id"],
		'nombre': p["title"],
		'precio': p["price"],
		'descripción': p["description"],
		'categoría': p["category"],
		'imágen': "imagenes/" + nombre_archivo,
		'rating': {'puntuación': p["rating"]["rate"], 'cuenta': p["rating"]["count"]}
	}

	prod = Producto(**product)
	
	#Inserta el producto en la colección de productos
	productos_collection.insert_one(prod.dict()) 		


compras_collection = tienda_db.compras  # Colección de las compras realizadas

#Obtiene las compras de la API
compras = getProductos('https://fakestoreapi.com/carts')

#Obtiene los usuarios de la API
usuarios = getProductos('https://fakestoreapi.com/users')

#Borra la colección de compras para que no se reinserten las mismas
compras_collection.drop()

#Establezco un contador para ir insertando los usuarios en las compras
user_counter = 0
for c in compras:
	comp = {
		'usuario': usuarios[user_counter]["email"],
		'fecha': datetime.now(),
		'productos': c["products"],
	}

	compra = Compra(**comp)

	#Inserta la compra en la colección de compras
	compras_collection.insert_one(compra.dict())

	user_counter += 1

# ----- CONSULTAS A REALIZAR
# ----- Electrónica entre 100 y 200€, ordenados por precio

print("-------Consulta 1: Electrónica entre 100 y 200€, ordenados por precio-------\n")

print(Queries.query1(productos_collection))


print("-------Consulta 2: Productos que contengan la palabra 'pocket' en la descripción-------\n")

print(Queries.query2(productos_collection))


print("-------Consulta 3: Productos con puntuación mayor de 4-------\n")

print(Queries.query3(productos_collection))


print("-------Consulta 4: Ropa de hombre, ordenada por puntuación -------\n")

print(Queries.query4(productos_collection))


print("-------Consulta 5: Facturación total -------\n")

print(Queries.query5(productos_collection, compras_collection))


print("-------Consulta 6: Facturación por categoría de producto -------\n")

print(Queries.query6(productos_collection, compras_collection))

#copia de la base de datos de la tienda
#docker run mongodump --host localhost --port 27017 --db tienda

	










	