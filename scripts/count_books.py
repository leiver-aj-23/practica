import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'misitio.settings')
import django
django.setup()

from miapp.models import Libro

print(Libro.objects.count())
