from django.db import models
from django.utils import timezone

# Create your models here.
class ValorTipo(models.Model):
	nombre = models.CharField(max_length=500)
	descripcion = models.CharField(max_length=1000,blank=True, null=True)
	padre = models.ForeignKey('self',blank=True, null=True,)
	activo = models.BooleanField(default=True)
	class Meta:
		verbose_name = u'Marcas, Categorias, Tipos de pago'
		verbose_name_plural = u'Marcas, Categorias, Tipos de pago'
	def __str__(self):
		return self.nombre

class Producto(models.Model):
	#Si no se coloca un codigo por defecto va a ser la llave primaria
	codigo = models.CharField(max_length=20,blank=True, null=True)
	nombre = models.CharField(max_length=200)
	tipoMarca = models.ForeignKey(ValorTipo,related_name='+',blank=True, null=True)
	valorCompra = models.IntegerField(default=0)
	valorVenta = models.IntegerField(default=0)
	ivaPorcentaje = models.IntegerField(default=0)
	#foto = models.FileField()
	descripcion = models.CharField(max_length=1000,blank=True, null=True)
	tipoCategoria = models.ForeignKey(ValorTipo,related_name='+')
	esServicio = models.BooleanField(default=False)
	def __str__(self):
		return self.nombre

class DivPolitica(models.Model):
	codigo = models.CharField(max_length=10)
	nombre = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=300)
	idPadre = models.ForeignKey('self',blank=True, null=True,)	
	class Meta:
		verbose_name = u'Ciudad'
		verbose_name_plural = u'Ciudades'
	def __str__(self):
		return self.nombre

class Constante(models.Model):
	nombre=models.CharField(max_length=50)
	descripcion=models.CharField(max_length=500,blank=True, null=True)
	valor=models.CharField(max_length=100)
	def __str__(self):
		return self.nombre