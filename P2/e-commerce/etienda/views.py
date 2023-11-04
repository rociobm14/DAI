from django.shortcuts import render, redirect
from django.http import HttpResponse
from .queries import productos_collection, GetCategories, getProductsByCategory, SearchProducts, getLastProductID
from .forms import ProductoForm
from .models import Producto

def index(request):
    context = {'products': productos_collection.find(),
               'categories': GetCategories(productos_collection)}
    return render(request, 'etienda/index.html', context)

def search(request):
    context = {'search': request.GET.get('to_find', ''), 
               'products': SearchProducts(productos_collection, request.GET.get('to_find', '')),
               'categories': GetCategories(productos_collection)}
    
    return render(request, 'etienda/search.html', context)

def category(request,category):
    context = {'products': getProductsByCategory(productos_collection, category), 
               'categories': GetCategories(productos_collection), 
               'category': category}
    return render(request, 'etienda/category.html', context)

def newproduct(request):
    form = ProductoForm()
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre_archivo = handle_uploaded_file(request.FILES['imágen'])
            #construyo el producto
            p = {
                "id_producto": getLastProductID(productos_collection)+1,
                "nombre": form.cleaned_data["nombre"],
                "precio": form.cleaned_data["precio"],
                "descripción": form.cleaned_data["descripción"],
                "categoría": form.cleaned_data["categoría"],
                "imágen": "imagenes/" + nombre_archivo,
                "rating": {'puntuación':0.0, 'cuenta': 1.0}
            }
            product = Producto(**p)
            
            #Inserta el producto en la BD
            productos_collection.insert_one(product.model_dump())
            
            return redirect('index')
        
    context = {'id': getLastProductID(productos_collection),
               'form': form,
               'categories': GetCategories(productos_collection)}
    return render(request, 'etienda/newproduct.html', context)
            
            
def handle_uploaded_file(f):
    path = "imagenes/" + f.name
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f.name
    