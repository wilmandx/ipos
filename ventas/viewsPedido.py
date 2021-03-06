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
def venta_desktop(request,nroFactura=None):
	nroFactura=request.GET.get('nroFact',None)
	print(get_default_timezone())
	ventaMaestro=None
	if nroFactura!=None : 
		#si viene con una m es una mesa
		if nroFactura[0]=='m':
			#buscar pedido en estado sin pagar con la mesa m
			try:
				ventaMaestro=VentaMaestro.objects.get(mesa=nroFactura[1:])
			except VentaMaestro.DoesNotExist:
				ventaMaestro=None
		else:
			#buscar por el numero de factura
			try:
				ventaMaestro=VentaMaestro.objects.get(numFactura=nroFactura)
			except VentaMaestro.DoesNotExist:
				ventaMaestro=None
	#Consultar los detalles
	listDetalles=None
	if(ventaMaestro!=None):
		listDetalles=ventaMaestro.ventadetalle_set.all()
	else:
		#crear un ventaMaestro con valores por defecto...cliente y vendedor
		ventaMaestro=VentaMaestro()
		ventaMaestro.cliente=User.objects.get(id=2)
		ventaMaestro.vendedor=request.user
	#Calcular el total para cada detalle y total general
	dictTotales={}
	granTotal=0
	ivaTotal=0
	ivaTmp=100
	if listDetalles!=None:
		for detalle in listDetalles:
			dictTotales[detalle.id]=(detalle.valorUni*detalle.cantidad)-detalle.descuento
			granTotal=granTotal+dictTotales[detalle.id]
			if detalle.iva==0 :
				ivaTmp=100
			else:
				ivaTmp=detalle.iva
			ivaTotal=ivaTotal+(dictTotales[detalle.id]*ivaTmp)/100
	dictTotales['granTotal']=granTotal
	dictTotales['ivaTotal']=ivaTotal
	dictTotales['subTotal']=granTotal-ivaTotal

	context = {'message':'ok','ventaMaestro':ventaMaestro,'listDetalles':listDetalles,'dictTotales':dictTotales}
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
def clientes(request):
	query = request.GET.get('q','')
	if(len(query) > 0):
		results = User.objects.filter(Q(last_name__icontains=query)|Q(first_name__icontains=query))
		result_list = []
		for item in results:
			result_list.append({'id':item.id,'nombre_completo':item.last_name+' '+item.first_name})
	else:
		result_list = []
	response_text = json.dumps(result_list, separators=(',',':'))
	return HttpResponse(response_text, content_type="application/json")

@login_required
def vendedores(request):
	query = request.GET.get('q','')
	if(len(query) > 0):
		results = User.objects.filter(Q(last_name__icontains=query)|Q(first_name__icontains=query))
		result_list = []
		for item in results:
			result_list.append({'id':item.id,'nombre_completo':item.last_name+' '+item.first_name})
	else:
		result_list = []
	response_text = json.dumps(result_list, separators=(',',':'))
	return HttpResponse(response_text, content_type="application/json")

@login_required
def codproducto(request):
	query = request.GET.get('q','')
	if(len(query) > 0):
		results = Producto.objects.filter(codigo__icontains=query)
		result_list = []
		for item in results:
			result_list.append({'id':item.id,'nombre':item.nombre,'codigo':item.codigo,'valorVenta':item.valorVenta,'iva':item.ivaPorcentaje})
	else:
		result_list = []
	response_text = json.dumps(result_list, separators=(',',':'))
	return HttpResponse(response_text, content_type="application/json")

@login_required
def nomproducto(request):
	query = request.GET.get('q','')
	if(len(query) > 0):
		results = Producto.objects.filter(nombre__icontains=query)
		result_list = []
		for item in results:
			result_list.append({'id':item.id,'nombre':item.nombre,'codigo':item.codigo,'valorVenta':item.valorVenta,'iva':item.ivaPorcentaje})
	else:
		result_list = []
	response_text = json.dumps(result_list, separators=(',',':'))
	return HttpResponse(response_text, content_type="application/json")

@login_required
def savePedido(request,anyway=None):
	#Validar si se debe guardar anyway
	#request.GET.get('anyway')
	if anyway==None:
		#Buscar si ya esta esa mesa con un pedido sin pagar
		idMaestroDetalle=buscarPedido(int((request.POST['mesa_p'],'0')[request.POST['mesa_p']=='']))
		if idMaestroDetalle:
			response_text = {'code':'01'}#Ya existe un pedido para la mesa sin pagar
			return HttpResponse(json.dumps(response_text), content_type="application/json")
	idFactura = None
	if request.POST['idFactura']!='':
		idFactura=int(request.POST['idFactura'])
		factura=VentaMaestro.objects.get(id=idFactura)
	else:
		factura=VentaMaestro()
	factura.cliente=User(id=(int(request.POST['idcliente_p']),1)[request.POST['idcliente_p']==''])
	factura.vendedor=User(id=(int(request.POST['idvendedor_p']),1)[request.POST['idvendedor_p']==''])
	factura.cajero=request.user
	#factura.valorPropina=int((request.POST['propina_p'],'0')[request.POST['propina_p']==''])
	factura.mesa=int((request.POST['mesa_p'],'0')[request.POST['mesa_p']==''])
	factura.save()
	df = DateFormat(factura.fechaVenta)
	response_text = {'code':'00','nroFactura':factura.id,'fechaVenta':df.format('d/M/Y'),'horaVenta':df.format('h:i A')}
	return HttpResponse(json.dumps(response_text), content_type="application/json")

def buscarPedido(nroMesa):
	lista=VentaMaestro.objects.filter(mesa=nroMesa,pagoventamaestro__valorPago__gt=0)
	return len(lista)

@login_required
def saveDetalle(request):
	factura=None

	if request.POST['idFacturaD']!='':
		idFactura=int(request.POST['idFacturaD'])
		factura=VentaMaestro.objects.get(id=idFactura)
	
	if request.POST['iddetalle_p']!='':
		idDetalle=int(request.POST['iddetalle_p'])
		ventaDetalle=VentaDetalle.objects.get(id=idDetalle)
	else:
		ventaDetalle=VentaDetalle()

	idProducto=int(request.POST['idproducto_p'])
	ventaDetalle.ventaMaestro=factura
	ventaDetalle.producto=Producto(id=idProducto)
	ventaDetalle.cantidad=int(request.POST['cantidad_p'])
	ventaDetalle.valorUni=int(request.POST['unitario_p'])
	ventaDetalle.iva=int(request.POST['valori_p'])
	ventaDetalle.descuento=int(request.POST['descuento_p'])
	ventaDetalle.save()
	response_text = {'idDetalle':ventaDetalle.id}
	return HttpResponse(json.dumps(response_text), content_type="application/json")

@login_required
def deleteDetalle(request,id):
	ventaDetalle=VentaDetalle.objects.get(id=id)
	ventaDetalle.delete()
	response_text = {'code':'00'}
	return HttpResponse(json.dumps(response_text), content_type="application/json")

@login_required
def pagarPedido(request):
	idFactura = None
	print("id factura="+request.POST['idFactura'])
	if request.POST['idFactura']!='':
		idFactura=int(request.POST['idFactura'])
		factura=VentaMaestro.objects.get(id=idFactura)
	else:
		response_text = {'code':'01'}#No se envio un identificador de pedido
		return HttpResponse(json.dumps(response_text), content_type="application/json")
	pago=PagoVentaMaestro()
	pago.ventaMaestro=factura
	pago.valorPago=(int(request.POST['vlr-efectivo']),0)[request.POST['vlr-efectivo']=='']
	pago.tipoMedioPago=ValorTipo(id=1)
	pago.save()
	factura.valorPropina=int((request.POST['propina_p'],'0')[request.POST['propina_p']==''])
	factura.descuento=int((request.POST['descuento_p'],'0')[request.POST['descuento_p']==''])
	factura.save()
	response_text = {'code':'00'}
	return HttpResponse(json.dumps(response_text), content_type="application/json")