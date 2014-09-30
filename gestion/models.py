from django.db import models
from django.utils import timezone

# Create your models here.
class ValorTipo(models.Model):
	nombre = models.CharField(max_length=500)
	descripcion = models.CharField(max_length=3000)
	padre = models.ForeignKey('self',blank=True, null=True,)
	activo = models.BooleanField(default=True)
	def __str__(self):
		return self.nombre

class Producto(models.Model):
	nombre = models.CharField(max_length=200)
	tipoMarca = models.ForeignKey(ValorTipo,related_name='+')
	precio = models.IntegerField(default=0)
	valorVenta = models.IntegerField(default=0)
	iva = models.IntegerField(default=0)
	#foto = models.FileField()
	descripcion = models.CharField(max_length=1000)
	tipoCategoria = models.ForeignKey(ValorTipo,related_name='+')
	def __str__(self):
		return self.nombre

class DivPolitica(models.Model):
	codigo = models.CharField(max_length=10)
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=300)
	idPadre = models.ForeignKey('self',blank=True, null=True,)	