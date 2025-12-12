import os
import sys
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'misitio.settings')
import django
django.setup()

from miapp.models import Libro

def info(msg):
    print(msg)

timestamp = int(time.time())
title = f"TEST_AUTOMATION_{timestamp}"

info(f"Count before: {Libro.objects.count()}")

# Create
lib = Libro.objects.create(
    titulo=title,
    autor='Auto Tester',
    descripcion='Creado por script de prueba',
    resumen='Resumen de prueba',
    editorial='TestPub',
    año=2025,
    categoria='Libros',
    imagen_url='',
    stock=5,
)
info(f"Created id={lib.id} titulo={lib.titulo}")
info(f"Count after create: {Libro.objects.count()}")

# Modify
lib.titulo = title + '_MOD'
lib.stock = 10
lib.save()
info(f"Modified id={lib.id} new_titulo={lib.titulo} new_stock={lib.stock}")

# Verify read
read = Libro.objects.filter(id=lib.id).first()
info(f"Read back: id={read.id} titulo={read.titulo} stock={read.stock}")

# Delete
lib.delete()
info('Deleted created book')
info(f"Count after delete: {Libro.objects.count()}")

sys.exit(0)
