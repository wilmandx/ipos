from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion.models import ValorTipo,Producto
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from ventas.models import VentaMaestro,VentaDetalle

# Create your views here.
class Categoria:
	listProductos=[]

@login_required
def venta_desktop(request,nroFactura=None):
	ventaMaestro=None
	if nroFactura!=None : 
		#si viene con una m es una mesa
		if nroFactura[0]=='m':
			#buscar pedido en estado sin pagar con la mesa m
			try:
				ventaMaestro=VentaMaestro.objects.get(numFactura=nroFactura[1:])
			except VentaMaestro.DoesNotExist:
				ventaMaestro=None
		else:
			#buscar por el numero de factura
			try:
				ventaMaestro=VentaMaestro.objects.get(numFactura=nroFactura)
			except VentaMaestro.DoesNotExist:
				ventaMaestro=None
	context = {'message':'ok','ventaMaestro':ventaMaestro}
	return render(request, 'venta.html',context)

@login_required
def venta_mobile(request):
	list_cate_prod={}
	list_categories=ValorTipo.objects.filter(padre=1)
	list_productos=Producto.objects.all()
	for producto in list_productos:
		for categoria in list_categories:
			if categoria.id==producto.tipoCategoria.id :
				if categoria.id in list_cate_prod :
					temp=list_cate_prod[categoria.id]
				else :
					temp=Categoria()
					temp.listProductos=[]
				temp.tipoCategoria=categoria
				temp.listProductos.append(producto)
				list_cate_prod[categoria.id]=temp

	context = {'message':'ok','list_categories':list_cate_prod}
	return render(request, 'mobile/venta.html',context)

@login_required
def listar(request):
    context = {'message':'ok'}
    return render(request, 'listar/pedido.html',context)

@login_required
def clientes(request):
	query = request.GET.get('q','')
	if(len(query) > 0):
		results = User.objects.filter(first_name__istartswith=query)
		result_list = []
		for item in results:
			result_list.append({'nombre_completo':item.first_name+' '+item.last_name})
	else:
		result_list = []
	response_text = json.dumps(result_list, separators=(',',':'))
	return HttpResponse(response_text, content_type="application/json")

@login_required
def savePedido(request):
	idFactura = None
	if request.POST['idFactura']!='':
		idFactura=int(request.POST['idFactura'])
		factura=VentaMaestro.objects.get(id=idFactura)
	else:
		factura=VentaMaestro()
	factura.cliente=User(id=1)
	factura.vendedor=User(id=1)
	#factura.numFactura=1
	valorPropina=(request.POST['propina'],'10')[request.POST['propina']=='']
	factura.valorPropina=int(valorPropina)
	factura.save()
	#Guardar los detalles
	ventaDetalle=VentaDetalle()
	ventaDetalle.ventaMaestro=factura
	ventaDetalle.producto=Producto(id=1)
	ventaDetalle.cantidad=int(request.POST['cantidad_p'])
	ventaDetalle.save()
	response_text = {'nroFactura':factura.id}
	return HttpResponse(json.dumps(response_text), content_type="application/json")