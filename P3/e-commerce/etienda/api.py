from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema



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
	
# @api.get("/products", tags=['Get list of products'],  response={202: list[ProductSchema]})
# def get_products_api(request, since:int, to:int):
#     return 202, get_products()[since:to]

# @api.post("/products", tags=['Add product'], response={202: list[ProductSchema], 404:ErrorSchema})
# def create_product_api(request, payload: ProductSchemaIn):
#     try:
#         result = create_product(payload)
#         return 202, result
    
#     except:
#         return 404, {'message': 'could not create product'}
        


    
