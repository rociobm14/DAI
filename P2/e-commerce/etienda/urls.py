from django.urls import path

from . import views

urlpatterns = [
    
    path("", views.index, name="index"),
    path("Query1/", views.Query1, name="Query1"),
    path("Query2/", views.Query2, name="Query2"),
    path("Query3/", views.Query3, name="Query3"),
    path("Query4/", views.Query4, name="Query4"),
    path("Query5/", views.Query5, name="Query5"),
    path("Query6/", views.Query6, name="Query6"),
    
]

