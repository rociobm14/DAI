from django.shortcuts import render
from django.http import HttpResponse
from .queries import query1, query2, query3, query4, query5, query6, productos_collection, compras_collection, GetCategories

# Create your views here

def index(request):
    context = {'products': productos_collection.find(), 'categories': GetCategories(productos_collection)}
    return render(request, 'etienda/index.html', context)

def categories(request):
    context = {'categories': GetCategories(productos_collection)}
    return render(request, 'etienda/categories.html', context)

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
