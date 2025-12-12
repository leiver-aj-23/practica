from django.db import models

# Create your models here.
class Practica(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    imagen_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.username


class Prestamo(models.Model):
    book_id = models.IntegerField()
    book_title = models.CharField(max_length=255)
    borrower_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=50)
    document_number = models.CharField(max_length=100)
    days = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prestamo {self.book_title} por {self.borrower_name}"


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    autor = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    resumen = models.TextField(blank=True, null=True)
    editorial = models.CharField(max_length=255, blank=True, null=True)
    año = models.IntegerField(blank=True, null=True)
    categoria = models.CharField(max_length=200, default='Libros')
    imagen_url = models.URLField(max_length=500, blank=True, null=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.titulo