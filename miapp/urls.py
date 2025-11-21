from django.urls import path
from . import views

urlpatterns = [
    path( "home/", views.saludo,),
    path( "hello/", views.vista, name="principal"),
    path( "index/", views.lala,  name="secundario"),
]