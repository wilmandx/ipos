from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from gestion.models import ValorTipo,Producto

# Create your views here.
class Categoria:
	listProductos=[]

@login_required
def venta_desktop(request):
    context = {'message':'ok'}
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
