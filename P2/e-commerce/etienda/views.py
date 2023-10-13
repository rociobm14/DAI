from django.shortcuts import render
from django.http import HttpResponse
from .queries import query1, query2, query3, query4, query5, query6, productos_collection, compras_collection

# Create your views here

def index(request):
    html = """
    <body>
        <h1>Práctica 2 DAI: Django Framework</h1>
        <ol>
            <li> <a href="Query1/">Consulta 1: Electrónica entre 100 y 200€, ordenados por precio</a> </li>
            <li> <a href="Query2/">Consulta 2: Productos que contengan la palabra 'pocket' en la descripción</a> </li>
            <li> <a href="Query3/">Consulta 3: Productos con puntuación mayor de 4</a> </li>
            <li> <a href="Query4/">Consulta 4:Ropa de hombre, ordenada por puntuación </a> </li>
            <li> <a href="Query5/">Consulta 5: Facturación total</a> </li>
            <li> <a href="Query6/">Consulta 6: Facturación por categoría de producto</a> </li>
        </ol>
    </body>

    """
    return HttpResponse(html)

def Query1(request):
    salida = query1(productos_collection)
    return HttpResponse(salida, content_type="text/plain")

def Query2(request):
    salida = query2(productos_collection)
    return HttpResponse(salida, content_type="text/plain")

def Query3(request):
    salida = query3(productos_collection)
    return HttpResponse(salida, content_type="text/plain")

def Query4(request):
    salida = query4(productos_collection)
    return HttpResponse(salida, content_type="text/plain")

def Query5(request):
    salida = query5(productos_collection, compras_collection)
    return HttpResponse(salida, content_type="text/plain")

def Query6(request):
    salida = query6(productos_collection, compras_collection)
    return HttpResponse(salida, content_type="text/plain") 