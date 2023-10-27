from django.shortcuts import render
from django.http import HttpResponse
from .queries import query1, query2, query3, query4, query5, query6, productos_collection, compras_collection, GetCategories

# Create your views here

def index(request):
    context = {'products': productos_collection.find(), 'categories': GetCategories(productos_collection)}
    return render(request, 'etienda/index.html', context)

def category(request,category):
    context = {'categories': GetCategories(productos_collection), 'category': category}
    return render(request, 'etienda/category.html', context)

