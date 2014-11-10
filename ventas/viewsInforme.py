from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion.models import ValorTipo,Producto
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from ventas.models import VentaMaestro,VentaDetalle,PagoVentaMaestro
from django.utils.dateformat import DateFormat
from django.db.models import Q
from django.utils.timezone import get_default_timezone

# Create your views here.
class Categoria:
	listProductos=[]

@login_required
def listar(request):
    context = {'message':'ok'}
    return render(request, 'listar/pedido.html',context)