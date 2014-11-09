from django.db import models
from gestion.models import ValorTipo
from gestion.models import Producto
from django.contrib.auth.models import User

# Create your models here.
class VentaMaestro(models.Model):
	numFactura = models.IntegerField(default=0)
	fechaVenta = models.DateTimeField(auto_now_add=True)
	cliente = models.ForeignKey(User,related_name='+')
	vendedor = models.ForeignKey(User,related_name='+')
	cajero = models.ForeignKey(User,related_name='+')
	mesa = models.IntegerField(default=1)
	valorPropina = models.IntegerField(default=0)
	descuento = models.IntegerField(default=0)
	nroAprobacionTC = models.IntegerField(default=0)

class VentaDetalle(models.Model):
	producto = models.ForeignKey(Producto)
	ventaMaestro = models.ForeignKey(VentaMaestro)
	cantidad = models.IntegerField(default=1)
	valorUni = models.IntegerField(default=0)
	iva = models.IntegerField(default=0)
	descuento = models.IntegerField(default=0)
	observaciones = models.TextField(blank=True, null=True)

class PagoVentaMaestro(models.Model):
	ventaMaestro = models.ForeignKey(VentaMaestro)
	valorPago = models.IntegerField(default=0)
	tipoMedioPago = models.ForeignKey(ValorTipo)