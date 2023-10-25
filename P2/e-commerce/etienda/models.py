from django.db import models
from pydantic import BaseModel, FilePath, Field, EmailStr, field_serializer, field_validator
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests, pathlib

def getProductos(api):
	response = requests.get(api)
	return response.json()
				
# Esquema de la BD

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
	imágen: FilePath | None
	rating: Nota

	@field_serializer('imágen')
	def serializaPath(self, val) -> str:
		if type(val) is pathlib.PosixPath:
			return str(val)
		return val	
	
	#Valida que el nombre empiece por mayúscula
	@field_validator('nombre')
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
