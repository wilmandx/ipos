from django.db import models
from django.utils import timezone
from gestion.models import ValorTipo
from gestion.models import Producto
from django.contrib.auth.models import User

# Create your models here.
class VentaMaestro(models.Model):
	numFactura = models.IntegerField(default=0)
	numRecibo = models.IntegerField(default=0)
	fechaVenta = models.DateTimeField(auto_now_add=True)
	cliente = models.ForeignKey(User,related_name='+')
	vendedor = models.ForeignKey(User,related_name='+')
	observaciones = models.TextField()
	valorPropina = models.IntegerField(default=0)
	nroAprobacionTC = models.IntegerField(default=0)

class VentaDetalle(models.Model):
	producto = models.ForeignKey(Producto)
	ventaMaestro = models.ForeignKey(VentaMaestro)
	cantidad = models.IntegerField(default=0)
	valorUni = models.IntegerField(default=0)
	ivaPorcen = models.IntegerField(default=0)
	descuentoPorcen = models.IntegerField(default=0)

class PagoVentaMaestro(models.Model):
	idVentaMaestro = models.IntegerField(default=0)
	valorPago = models.IntegerField(default=0)
	idTipoMedioPago = models.ForeignKey(ValorTipo)