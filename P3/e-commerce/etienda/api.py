from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema
from .queries import get_products, create_product, get_product_by_id, modify_product_by_id, delete_product_by_id, modify_product_rating_by_id, product_by_id

import logging
logger = logging.getLogger(__name__)

api = NinjaExtraAPI()

class Rate(Schema):
	rate: float
	count: int
	
class ProductSchema(Schema):  # sirve para validar y para documentación
	id:    str
	title: str
	price: float
	description: str
	category: str
	image: str = None
	rating: Rate
	
	
class ProductSchemaIn(Schema): 
	title: str
	price: float
	description: str
	category: str
	rating: Rate
	
	
class ErrorSchema(Schema):
	message: str

#La he creado yo para mostrar mensajes válidos
class SuccessResponseSchema(Schema):
    message: str

#Muestra una lista de productos
@api.get("/getproducts", tags=['Get list of products'],  response={202: list[ProductSchema], 404:ErrorSchema})
def get_products_api(request, since:int, to:int):
    return 202, get_products()[since:to]

#Inserta un producto
@api.post("/addproduct", tags=['Add product'], response={202: SuccessResponseSchema, 404: ErrorSchema})
def create_product_api(request, payload: ProductSchemaIn):
    try:
        create_product(payload)
        return 202, {'message': 'Product created successfully'}
    
    except:
        return 404, {'message': 'Could not create product'}
    
#Muestra un detalle del producto
@api.get("/getproduct/{id}", tags=['Show product'], response={202: ProductSchema, 404: ErrorSchema})
def get_product(request, id:str):
    try:
        product = get_product_by_id(id)
        return 202, product
    
    except:
        return 404, {'message': 'the product could not be found'}
    
#modifica un producto dado un objeto de tipo productSchemaIn
@api.put("/modifyproduct/{id}", tags=['Modify product'], response = {202: ProductSchema, 404: ErrorSchema})
def modify_product(request, id: str, payload: ProductSchemaIn):
	try:
		product_updated = modify_product_by_id(id,payload)
		return 202, product_updated
	except:
		return 404, {'message': 'product could not be updated'}

#borra un producto de la BD
@api.delete("/deleteproduct/{id}", tags=['Delete product'], response = {202: SuccessResponseSchema, 404: ErrorSchema})
def delete_product(request, id:str):
	try:
		delete_product_by_id(id)
		return 202, {"message": "The product has been deleted succesfully"}

	except:
		return 404, {'message': 'The product could not be deleted'}

#modifica el rating de un producto
@api.put("/modifyrating/{id}/{rating}", tags=['Modify rating of product'], response={202: SuccessResponseSchema, 404: ErrorSchema})
def modify_rating(request, id: int, rating: int):
    try:
        modify_product_rating_by_id(id, rating)
        return 202, {"message": "the product rate has been updated succesfully"}
    
    except:
        return 404, {"message": "the product rate could not be modified"}
    

#obtiene el producto por el id por defecto
@api.get("/getproductbyid/{id}", tags=['Get product with normal id'], response={202: ProductSchema, 404: ErrorSchema})
def get_product(request, id:int):
    try:
        product = product_by_id(id)
        return 202, product
    
    except:
        return 404, {'message': 'the product could not be found'}


    

    
