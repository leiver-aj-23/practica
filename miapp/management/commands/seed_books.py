from django.core.management.base import BaseCommand
from miapp.models import Libro


class Command(BaseCommand):
    help = 'Seed database with one sample book per category (idempotent)'

    def handle(self, *args, **options):
        samples = [
            {"titulo": "Cien años de soledad", "autor": "Gabriel García Márquez", "categoria": "Libros", "editorial": "Sudamericana", "año": 1967, "resumen": "Novela clásica latinoamericana."},
            {"titulo": "Guía de Carrera Profesional", "autor": "María López", "categoria": "Carrera laboral", "editorial": "Profesional S.A.", "año": 2018, "resumen": "Consejos para el desarrollo profesional."},
            {"titulo": "Cálculo en una pasada", "autor": "James Stewart", "categoria": "Matemáticas", "editorial": "Cengage", "año": 2015, "resumen": "Manual para estudiantes de cálculo."},
            {"titulo": "Python para Principiantes", "autor": "Mark Lutz", "categoria": "Tecnología e informática", "editorial": "O'Reilly", "año": 2020, "resumen": "Introducción práctica a Python."},
            {"titulo": "Historia del Arte", "autor": "Ana Ruiz", "categoria": "Arte y humanidades", "editorial": "ArtePress", "año": 2012, "resumen": "Recorrido por los movimientos artísticos."},
            {"titulo": "Teoría Musical Básica", "autor": "Luis Martín", "categoria": "Música", "editorial": "Melodía Ediciones", "año": 2010, "resumen": "Fundamentos de la música."},
            {"titulo": "Métodos de Enseñanza", "autor": "Rosa Pérez", "categoria": "Educación y pedagogía", "editorial": "Educa", "año": 2016, "resumen": "Técnicas pedagógicas modernas."},
            {"titulo": "Espiritualidad Práctica", "autor": "Sergio Díaz", "categoria": "Religión y espiritualismo", "editorial": "Alma", "año": 2005, "resumen": "Reflexiones y prácticas espirituales."},
            {"titulo": "Gestión Personal Efectiva", "autor": "Carla Gómez", "categoria": "Administración y gestión personal", "editorial": "AdminPub", "año": 2019, "resumen": "Herramientas para la gestión personal."},
        ]

        created = 0
        skipped = 0
        for s in samples:
            obj, was_created = Libro.objects.get_or_create(
                titulo=s['titulo'],
                defaults={
                    'autor': s.get('autor',''),
                    'categoria': s.get('categoria','Libros'),
                    'editorial': s.get('editorial',''),
                    'año': s.get('año', None),
                    'resumen': s.get('resumen',''),
                    'descripcion': s.get('resumen',''),
                    'imagen_url': s.get('imagen_url',''),
                    'stock': s.get('stock', 1),
                }
            )
            if was_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created: {obj.titulo} ({obj.categoria})"))
            else:
                skipped += 1
                self.stdout.write(self.style.NOTICE(f"Skipped (exists): {obj.titulo}"))

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created: {created}, Skipped: {skipped}"))
