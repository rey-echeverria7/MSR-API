from django.db import models

# Create your models here.
class Refaccion(models.Model):
    codigo = models.CharField(max_length=50)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=100)
    precio = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre