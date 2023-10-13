from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("C1/", views.C1, name="C1"),
    path("C2/", views.C2, name="C2"),
    path("C3/", views.C3, name="C3"),
    path("C4/", views.C4, name="C4"),
    path("C5/", views.C5, name="C5"),
    path("C6/", views.C6, name="C6"),
]
