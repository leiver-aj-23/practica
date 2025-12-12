from django.core.management.base import BaseCommand
from miapp.models import Practica

class Command(BaseCommand):
    help = 'Create or update admin user'

    def handle(self, *args, **options):
        username = 'admin'
        password = '12345'
        obj, created = Practica.objects.get_or_create(username=username, defaults={'password': password})
        if created:
            self.stdout.write(self.style.SUCCESS(f"Usuario '{username}' creado con contraseña '{password}'"))
        else:
            obj.password = password
            obj.save()
            self.stdout.write(self.style.SUCCESS(f"Usuario '{username}' ya existía. Contraseña actualizada a '{password}'"))
