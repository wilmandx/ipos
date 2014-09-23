from django.db import models

# Create your models here.
class Categoria(models.Model):
	nombre = models.CharField(max_length=200)
	descripcion = models.CharField(max_length=1000)
	def __str__(self):
		return self.nombre

class Producto(models.Model):
	nombre = models.CharField(max_length=200)
	descripcion = models.CharField(max_length=1000)
	precio = models.IntegerField(default=0)
	categoria = models.ForeignKey(Categoria)
	def __str__(self):
		return self.nombre
    
		