from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion.models import ValorTipo,Producto
from django.contrib.auth.models import User
from django.http import HttpResponse
import json
from ventas.models import VentaMaestro,VentaDetalle
from django.utils import formats

# Create your views here.
class Categoria:
	listProductos=[]

@login_required
def venta_desktop(request,nroFactura=None):
	nroFactura=request.GET.get('nroFact',None)
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
def listar(request):
    context = {'message':'ok'}
    return render(request, 'listar/pedido.html',context)

@login_required
def clientes(request):
	query = request.GET.get('q','')
	if(len(query) > 0):
		results = User.objects.filter(last_name__istartswith=query)
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
		results = User.objects.filter(last_name__istartswith=query)
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
		results = Producto.objects.filter(codigo__istartswith=query)
		result_list = []
		for item in results:
			result_list.append({'id':item.id,'nombre':item.nombre,'codigo':item.codigo,'valorVenta':item.valorVenta,'iva':item.ivaPorcentaje})
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
	factura.cliente=User(id=(int(request.POST['idcliente_p']),1)[request.POST['idcliente_p']==''])
	factura.vendedor=User(id=(int(request.POST['idvendedor_p']),1)[request.POST['idvendedor_p']==''])
	factura.valorPropina=int((request.POST['propina_p'],'0')[request.POST['propina_p']==''])
	factura.mesa=int((request.POST['mesa_p'],'0')[request.POST['mesa_p']==''])
	factura.save()

	response_text = {'nroFactura':factura.id,'fechaVenta':formats.date_format(factura.fechaVenta, "DATE_FORMAT"),'horaVenta':formats.date_format(factura.fechaVenta, "TIME_FORMAT")}
	return HttpResponse(json.dumps(response_text), content_type="application/json")

@login_required
def saveDetalle(request):
	factura=None
	if request.POST['idFacturaD']!='':
		idFactura=int(request.POST['idFacturaD'])
		factura=VentaMaestro.objects.get(id=idFactura)
	#Guardar los detalles
	idProducto=int(request.POST['idproducto_p'])
	ventaDetalle=VentaDetalle()
	ventaDetalle.ventaMaestro=factura
	ventaDetalle.producto=Producto(id=idProducto)
	ventaDetalle.cantidad=int(request.POST['cantidad_p'])
	ventaDetalle.valorUni=int(request.POST['unitario_p'])
	ventaDetalle.iva=int(request.POST['valori_p'])
	ventaDetalle.descuento=int(request.POST['descuento_p'])
	ventaDetalle.save()
	response_text = {'idDetalle':ventaDetalle.id}
	return HttpResponse(json.dumps(response_text), content_type="application/json")