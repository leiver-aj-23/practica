from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def saludo(request):
    return HttpResponse("Hola Mundo")

def vista(request):
    return render(request, "anime.html")

def lala(request):
    return render(request, "index.html")

