from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path('search/', views.search, name='search'),
    path('categories/<str:category>/', views.category, name='category'),
    
]

